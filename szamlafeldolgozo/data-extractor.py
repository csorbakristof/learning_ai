import argparse
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "local-model"
DEFAULT_PROMPT = """Olvasd el ezt a dokumentumot figyelmesen, és gyűjtsd ki JSON formátumban az alábbi mezőket.
Csak érvényes JSON-t adj vissza.
- szolgáltató_neve
- felhasználási_hely_címe
- szolgáltatás_megnevezése
- számla_kelte
- számla_összege

Ha egy adat nem látható a dokumentumban, az érték legyen "???".
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract PDFs from a ZIP archive, extract text and tables from each PDF, and send the content to LM Studio for JSON extraction."
    )
    parser.add_argument("--zip-path", required=True, help="Path to the input ZIP file.")
    parser.add_argument("--output-json", required=True, help="Path to save the combined JSON output.")
    parser.add_argument("--base-url", default=os.getenv("LM_STUDIO_BASE_URL", DEFAULT_BASE_URL), help="LM Studio base URL (default: http://localhost:1234/v1)")
    parser.add_argument("--model", default=os.getenv("LM_STUDIO_MODEL", DEFAULT_MODEL), help="LM Studio model name to call.")
    parser.add_argument("--api-key", default=os.getenv("LM_STUDIO_API_KEY", ""), help="Optional API key for LM Studio-compatible servers.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send along with the extracted PDF content.")
    return parser.parse_args()


def extract_pdf_content(pdf_path: Path) -> str:
    """Extract text and tables from a PDF using PyMuPDF first, with pdfplumber and pypdf fallbacks."""
    content_parts = []

    try:
        import fitz

        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text("text") or ""
                if page_text.strip():
                    content_parts.append(f"=== Page {page_num} text ===\n{page_text.strip()}")
    except Exception:
        content_parts = []

    if not content_parts:
        try:
            import pdfplumber
        except ImportError as exc:
            raise RuntimeError("pdfplumber is required. Install it with: pip install pdfplumber pypdf pymupdf") from exc

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    content_parts.append(f"=== Page {page_num} text ===\n{page_text.strip()}")

                tables = page.extract_tables() or []
                for table_idx, table in enumerate(tables, start=1):
                    cleaned_rows = []
                    for row in table:
                        if not row:
                            continue
                        cleaned_row = [cell.strip() if isinstance(cell, str) else "" for cell in row]
                        if any(cleaned_row):
                            cleaned_rows.append(cleaned_row)
                    if cleaned_rows:
                        content_parts.append(f"=== Page {page_num} table {table_idx} ===\n{json.dumps(cleaned_rows, ensure_ascii=False)}")

    if not content_parts:
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(pdf_path))
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    content_parts.append(f"=== Page {page_num} text ===\n{text.strip()}")
        except Exception as exc:
            raise RuntimeError(f"Could not extract any text or tables from {pdf_path.name}: {exc}") from exc

    if not content_parts:
        raise RuntimeError(f"No extractable content found in {pdf_path.name}")

    return "\n\n".join(content_parts).strip()


def _clean_llm_response(raw_text: str) -> str:
    """Remove reasoning tags and markdown fences from LM Studio responses before parsing JSON."""
    text = raw_text.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return text


def query_lm_studio(base_url: str, model: str, prompt: str, document_content: str, api_key: str) -> dict:
    """Send the extracted PDF content to an LM Studio-compatible chat completions endpoint."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a document extraction assistant. Return only valid JSON."},
            {"role": "user", "content": f"{prompt}\n\nDocument content:\n{document_content}"}
        ],
        "temperature": 0.1,
        "max_tokens": 2000,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=180)
    response.raise_for_status()

    data = response.json()
    raw_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    clean_text = _clean_llm_response(raw_text)

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_text}


def process_pdf_files(zip_path: str, output_path: str, base_url: str, model: str, api_key: str, prompt: str):
    results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        print(f"Extracting ZIP archive: {zip_path}")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir_path)

        pdf_files = sorted([p for p in temp_dir_path.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"])
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the ZIP archive.")

        print(f"Found {len(pdf_files)} PDF file(s) to process.")

        for idx, pdf_file in enumerate(pdf_files, start=1):
            relative_path = str(pdf_file.relative_to(temp_dir_path))
            print(f"\n[{idx}/{len(pdf_files)}] Processing: {relative_path}")
            try:
                extracted_content = extract_pdf_content(pdf_file)
                print(f" -> Extracted {len(extracted_content)} characters from {pdf_file.name}")
                answer = query_lm_studio(base_url, model, prompt, extracted_content, api_key)

                processed_entry = {
                    "source_metadata": {
                        "filename": pdf_file.name,
                        "relative_path": relative_path,
                    },
                    "analysis": answer,
                }
                print(f" -> LLM response for {pdf_file.name}: {json.dumps(answer, ensure_ascii=False, indent=2)}")
                results.append(processed_entry)
            except Exception as err:
                print(f" ERROR processing {relative_path}: {err}")
                results.append({
                    "source_metadata": {
                        "filename": pdf_file.name,
                        "relative_path": relative_path,
                    },
                    "error": str(err),
                })

    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, indent=2, ensure_ascii=False)

    print(f"\nCompleted! Combined output saved to: {output_path}")


if __name__ == "__main__":
    args = parse_args()
    process_pdf_files(
        zip_path=args.zip_path,
        output_path=args.output_json,
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        prompt=args.prompt,
    )
