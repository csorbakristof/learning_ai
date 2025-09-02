---
layout: project
title: "Bill Summarizer"
project_dir: "BillSummarizer"
status: "In Development"
release_url: ""
getting_started: |
  1. Navigate to the BillSummarizer directory
  2. Install dependencies: `pip install -r requirements.txt`
  3. Run the extractor: `python bill_extractor.py`
  4. Or use the batch file: `run_bill_extractor.bat`
user_guide: |
  The Bill Summarizer processes financial documents and extracts key information. 
  
  **Input**: PDF or image files of bills and invoices
  **Output**: Structured data in CSV format
  
  **Usage**:
  - Place your bill files in the input directory
  - Run the extraction script
  - Review the output in `final_test.csv`
  - Check `bill_extraction.log` for processing details
---

## Overview

The Bill Summarizer is an AI-powered tool designed to automatically extract and summarize key information from bills, invoices, and other financial documents. It uses OCR and natural language processing to identify important fields such as amounts, dates, vendor information, and line items.

## Features

- **Automated OCR**: Extracts text from PDF and image files
- **Smart Field Detection**: Identifies key financial information using AI
- **Batch Processing**: Handles multiple documents efficiently
- **CSV Export**: Outputs structured data for further analysis
- **Logging**: Detailed processing logs for troubleshooting

## Technical Details

- **Language**: Python
- **Dependencies**: Listed in `requirements.txt`
- **Input Formats**: PDF, PNG, JPG
- **Output Format**: CSV

## Current Status

This project is actively being developed. Current capabilities include basic text extraction and field identification. Future enhancements will include improved accuracy and support for additional document types.

## Examples

Sample input and output files are available in the `examples/` directory within the project folder.
