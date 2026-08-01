Create a python script which takes a zip file as input. Extracts all PDF files (from all subdirectories) and one-by-one.processes them using AnythingLLM: it uploads the file, sends a processing query which returns a JSON answer, and concatenates these JSON answers into a single file. It appends the path and filename to the individual answers before merging them.

## Prerequisites

``` bash
pip install requests
```

## Example start

``` bash
python process_zip_anythingllm.py \
  --zip-path "/path/to/documents.zip" \
  --output-json "/path/to/output.json" \
  --api-key "YOUR_ANYTHINGLLM_API_KEY" \
  --workspace-slug "my-workspace" \
  --prompt "Extract the document title, summary, and action items into a JSON object."
```
