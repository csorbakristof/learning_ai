Create a Python script which takes a ZIP file as input, extracts all PDF files from all subdirectories, and processes them one by one. For each PDF, the script uses a table-aware PDF extraction library to pull out text and tabular data, sends the extracted content together with a query to an LM Studio-compatible API endpoint, and merges the returned JSON answers into a single output file. Each result includes the source path and filename before being combined.

## Prerequisites

```bash
pip install requests pdfplumber pypdf pymupdf
```

## Example start

```bash
python data-extractor.py \
  --zip-path "/path/to/documents.zip" \
  --output-json "/path/to/output.json" \
  --base-url "http://localhost:1234/v1" \
  --model "local-model" \
  --prompt "Extract the document title, summary, and action items into a JSON object."
```

## Notes

- The script uses the LM Studio OpenAI-compatible chat completions endpoint directly.
- The PDF extraction step uses PyMuPDF first, with pdfplumber and pypdf as fallbacks, so text and table content are preserved as accurately as possible.
- If LM Studio is running locally, no API key is usually required.
