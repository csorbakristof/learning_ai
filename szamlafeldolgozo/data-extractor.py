import argparse
import json
import os
import re
import tempfile
import time
import zipfile
from pathlib import Path
import requests

# Default AnythingLLM configuration
DEFAULT_BASE_URL = "http://localhost:3001"
DEFAULT_PROMPT = """Olvasd el ezt a számla dokumentumot és gyűjtsd ki JSON formátumba az alábbi adatokat.
Csak tiszta JSON formátumot adj vissza.
- A szolgáltató neve.
- A Felhasználási hely címe (mint például 1115 Budapest, Bartók Béla út 129 . ép. 3.")
- A szolgáltatás megnevezése (mint például "Villamos energia elszámoló számla" vagy "Távhőszolgáltatási 1. részszámla" a dokumentum legelején.),
- Számla kelte (egy dátum string, mint például "Számla kelte: 2026.06.05"),
- A számla összege (Fizetendő összeg összesen)

Ha a kapott dokumentumból ezek az adatok nem nyerhetőek ki, a hiányzó mezők értéke legyen "???".
""";

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract PDFs from a ZIP file and process them individually with AnythingLLM."
    )
    parser.add_argument("--zip-path", required=True, help="Path to the input ZIP file.")
    parser.add_argument("--output-json", required=True, help="Path to save the combined JSON output.")
    parser.add_argument("--api-key", required=True, help="AnythingLLM API Key.")
    parser.add_argument(
        "--workspace-slug",
        default=os.getenv("ANYTHINGLLM_WORKSPACE_SLUG"),
        help="AnythingLLM workspace slug. Provide the actual slug from your workspace (for example: my-workspace)."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="AnythingLLM API Base URL (default: http://localhost:3001)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Query prompt to send for processing each PDF.")
    args = parser.parse_args()

    if not args.workspace_slug:
        parser.error("--workspace-slug is required and must be an existing AnythingLLM workspace slug.")

    return args


def _extract_document_location(res_data: dict, file_name: str) -> str:
    """Extract the document location returned by AnythingLLM after upload."""
    documents = res_data.get("documents") or []
    if not documents:
        raise RuntimeError(f"Upload response did not contain any document entries for {file_name}: {res_data}")

    first_doc = documents[0]
    location = first_doc.get("location")
    if not location and isinstance(first_doc.get("document"), dict):
        location = first_doc["document"].get("location")

    if not location:
        raise RuntimeError(f"Could not find a document location in upload response for {file_name}: {res_data}")

    return location


def upload_document(base_url: str, api_key: str, file_path: Path, workspace_slug: str) -> str:
    """
    Uploads a document to AnythingLLM and returns the document location used for querying.
    """
    url = f"{base_url.rstrip('/')}/api/v1/document/upload"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, "application/pdf")}
        data = {"addToWorkspaces": workspace_slug}
        response = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(f"Upload failed for {file_path.name}: HTTP {response.status_code}: {response.text.strip()}") from exc

    res_data = response.json()

    if res_data.get("success") and res_data.get("documents"):
        doc_location = _extract_document_location(res_data, file_path.name)
        return doc_location
    else:
        raise RuntimeError(f"Failed to upload document {file_path.name}: {res_data}")


def get_workspace_documents(base_url: str, api_key: str, workspace_slug: str) -> list[str]:
    """Return the document locations currently attached to a workspace."""
    url = f"{base_url.rstrip('/')}/api/v1/workspace/{workspace_slug}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception:
        return []

    res_data = response.json()
    document_locations = []
    if isinstance(res_data, dict):
        documents = res_data.get("documents") or []
        for item in documents:
            if isinstance(item, dict):
                location = item.get("location") or item.get("path")
                if location:
                    document_locations.append(location)
    return document_locations


def remove_from_workspace(base_url: str, api_key: str, workspace_slug: str, doc_location: str):
    """Remove a document from the workspace and any attached embeddings."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 1) Try the workspace embeddings delete endpoint.
    url = f"{base_url.rstrip('/')}/api/v1/workspace/{workspace_slug}/update-embeddings"
    payload = {"adds": [], "deletes": [doc_location]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except Exception:
        pass

    # 2) Try deleting the document directly from the document API.
    doc_url = f"{base_url.rstrip('/')}/api/v1/document"
    try:
        response = requests.delete(doc_url, headers={"Authorization": f"Bearer {api_key}"}, params={"location": doc_location}, timeout=60)
        response.raise_for_status()
    except Exception:
        pass


def clear_workspace_documents(base_url: str, api_key: str, workspace_slug: str):
    """Remove any documents already attached to the workspace before processing the ZIP."""
    document_locations = get_workspace_documents(base_url, api_key, workspace_slug)
    if not document_locations:
        return

    print(f" -> Deleting workspace documents: {document_locations}")
    for doc_location in document_locations:
        remove_from_workspace(base_url, api_key, workspace_slug, doc_location)


def _clean_llm_response(raw_text: str) -> str:
    """Remove reasoning tags and markdown fences from AnythingLLM responses before parsing JSON."""
    text = raw_text.strip()

    # Remove <think>...</think> blocks, including multi-line reasoning.
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove leading/trailing whitespace around markdown code fences.
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return text


def query_workspace(base_url: str, api_key: str, workspace_slug: str, prompt: str, doc_location: str | None = None) -> dict:
    """
    Sends a query prompt to the workspace chat endpoint.
    """
    url = f"{base_url.rstrip('/')}/api/v1/workspace/{workspace_slug}/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": prompt,
        "mode": "query"
    }
    print(f" -> Prompt sent to LLM: {prompt}")
    if doc_location:
        payload["documentLocations"] = [doc_location]
        payload["documents"] = [doc_location]

    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(f"Query failed for workspace '{workspace_slug}': HTTP {response.status_code}: {response.text.strip()}") from exc

    res_data = response.json()
    raw_text = res_data.get("textResponse", "")
    clean_text = _clean_llm_response(raw_text)

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_text}


def process_pdf_files(zip_path: str, output_path: str, api_key: str, workspace_slug: str, base_url: str, prompt: str):
    results = []

    print("Preparing workspace for isolated document queries...")
    clear_workspace_documents(base_url, api_key, workspace_slug)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        print(f"Extracting ZIP archive: {zip_path}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir_path)

        # Recursively find all PDF files within all subdirectories
        pdf_files = sorted([p for p in temp_dir_path.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"])

        print(f"Found {len(pdf_files)} PDF file(s) to process.")

        active_doc_location = None
        for idx, pdf_file in enumerate(pdf_files, start=1):
            relative_path = str(pdf_file.relative_to(temp_dir_path))
            print(f"\n[{idx}/{len(pdf_files)}] Processing: {relative_path}")

            if active_doc_location:
                print(" -> Removing previous document from workspace before processing the next file...")
                remove_from_workspace(base_url, api_key, workspace_slug, active_doc_location)
                active_doc_location = None

            doc_location = None
            try:
                # 1. Upload Document
                print(" -> Uploading document...")
                doc_location = upload_document(base_url, api_key, pdf_file, workspace_slug)
                print(f" -> Uploaded document location: {doc_location}")
                active_doc_location = doc_location

                # 2. Query AnythingLLM with the uploaded document already attached to the workspace
                print(" -> Querying AnythingLLM...")
                answer = query_workspace(base_url, api_key, workspace_slug, prompt, doc_location)

                # 3. Format and append response metadata
                processed_entry = {
                    "source_metadata": {
                        "filename": pdf_file.name,
                        "relative_path": relative_path
                    },
                    "analysis": answer
                }
                print(f" -> LLM response for {pdf_file.name}: {json.dumps(answer, ensure_ascii=False, indent=2)}")
                results.append(processed_entry)

            except Exception as err:
                print(f" ERROR processing {relative_path}: {err}")
                results.append({
                    "source_metadata": {
                        "filename": pdf_file.name,
                        "relative_path": relative_path
                    },
                    "error": str(err)
                })
            finally:
                if doc_location:
                    remove_from_workspace(base_url, api_key, workspace_slug, doc_location)
                    if active_doc_location == doc_location:
                        active_doc_location = None

    if active_doc_location:
        print(" -> Cleaning up the last document from workspace...")
        remove_from_workspace(base_url, api_key, workspace_slug, active_doc_location)

    # Save aggregated results
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, indent=2, ensure_ascii=False)

    print(f"\nCompleted! Combined output saved to: {output_path}")


if __name__ == "__main__":
    args = parse_args()
    process_pdf_files(
        zip_path=args.zip_path,
        output_path=args.output_json,
        api_key=args.api_key,
        workspace_slug=args.workspace_slug,
        base_url=args.base_url,
        prompt=args.prompt
    )
