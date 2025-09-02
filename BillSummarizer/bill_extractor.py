#!/usr/bin/env python3
"""
Hungarian Bill Information Extractor

This script extracts key information from Hungarian utility bills in PDF format:
- Amount (összeg)
- Issue date (számla kelte)
- Provider company (szolgáltató)
- Consumer address (fogyasztó címe)

The script uses text extraction with Hungarian keyword detection and pattern matching fallbacks.
"""

import os
import csv
import pdfplumber
import re
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

class BillExtractor:
    """Extract information from Hungarian utility bills in PDF format"""
    
    def __init__(self, log_level=logging.INFO):
        """Initialize the bill extractor with logging configuration"""
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bill_extraction.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Hungarian keywords for field extraction
        self.keywords = {
            'amount': ['fizetendő', 'összeg', 'végösszeg', 'teljes összeg', 'bruttó összeg'],
            'date': ['számla kelte', 'kiállítás dátuma', 'számlakelte', 'dátum'],
            'provider': ['szolgáltató neve', 'szolgáltató', 'kiállító', 'cégnév'],
            'address': ['felhasználási hely címe', 'fogyasztási hely', 'címzett címe', 'cím']
        }
        
        # Patterns for fallback extraction
        self.patterns = {
            'amount': re.compile(r'(\d{1,3}(?:\s?\d{3})*(?:[.,]\d{2})?)\s*Ft', re.IGNORECASE),
            'date': re.compile(r'(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})'),
            'address': re.compile(r'(\d{4}\s+[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű\s]+,?[^,\n]{10,80})', re.UNICODE),
            'provider': re.compile(r'([A-ZÁÉÍÓÖŐÚÜŰ][A-Za-záéíóöőúüű\s]+(?:Kft|Zrt|Bt|Nonprofit)[.]?)', re.UNICODE)
        }

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file using pdfplumber"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            self.logger.error(f"Failed to extract text from {pdf_path}: {str(e)}")
            return ""

    def find_field_by_keywords(self, text: str, field_type: str) -> Tuple[Optional[str], float]:
        """
        Find field value using Hungarian keywords
        Returns: (value, confidence_score)
        """
        keywords = self.keywords.get(field_type, [])
        text_lower = text.lower()
        
        for keyword in keywords:
            keyword_pos = text_lower.find(keyword.lower())
            if keyword_pos != -1:
                # Extract text after the keyword
                after_keyword = text[keyword_pos + len(keyword):]
                
                if field_type == 'amount':
                    # Try different Hungarian number formats - most specific first
                    patterns = [
                        r'[:\s]*(\d{1,3}\.\d{3})\s*Ft',                  # 6.267 Ft (period thousands separator)
                        r'[:\s]*(\d{1,3}\s+\d{3})\s*Ft',                 # 4 225 Ft (space thousands separator) 
                        r'[:\s]*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*Ft',  # 1.234,56 Ft (Hungarian standard with decimals)
                        r'[:\s]*(\d{1,3}(?:\s\d{3})*(?:,\d{2})?)\s*Ft',  # 1 234,56 Ft (space separated with decimals)
                        r'[:\s]*(\d+(?:,\d{2})?)\s*Ft',                  # 1234,56 Ft or 1234 Ft
                        r'[:\s]*(\d+)\s*Ft'                              # Simple format
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, after_keyword[:100])
                        if match:
                            amount = match.group(1)
                            # Convert Hungarian format to standard: remove spaces, handle periods/commas
                            amount = amount.replace(' ', '')
                            if '.' in amount and ',' in amount:
                                # Format like 1.234,56 - period is thousands separator
                                amount = amount.replace('.', '').replace(',', '.')
                            elif '.' in amount and len(amount.split('.')[-1]) == 3:
                                # Format like 6.267 - period is thousands separator
                                amount = amount.replace('.', '')
                            elif ',' in amount:
                                # Format like 1234,56 - comma is decimal separator
                                amount = amount.replace(',', '.')
                            return amount, 0.9
                
                elif field_type == 'date':
                    match = re.search(r'[:\s]*(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})', after_keyword[:50])
                    if match:
                        return self.normalize_date(match.group(1)), 0.9
                
                elif field_type == 'provider':
                    # Extract text in the next 100 characters after keyword
                    lines = after_keyword[:200].split('\n')
                    for line in lines[:3]:  # Check first 3 lines
                        line = line.strip()
                        if len(line) > 5 and any(suffix in line for suffix in ['Kft', 'Zrt', 'Bt', 'Nonprofit']):
                            return line, 0.9
                
                elif field_type == 'address':
                    # Extract address from next few lines
                    lines = after_keyword[:300].split('\n')
                    for line in lines[:5]:  # Check first 5 lines
                        line = line.strip()
                        if re.match(r'\d{4}\s+[A-ZÁÉÍÓÖŐÚÜŰ]', line):
                            # Combine multiple lines if address continues
                            full_address = line
                            return full_address, 0.9
        
        return None, 0.0

    def extract_by_patterns(self, text: str, field_type: str) -> Tuple[Optional[str], float]:
        """Extract field using regex patterns as fallback"""
        pattern = self.patterns.get(field_type)
        if not pattern:
            return None, 0.0
        
        matches = pattern.findall(text)
        if matches:
            if field_type == 'amount':
                # Find the largest amount (likely the total)
                amounts = []
                for match in matches:
                    clean_amount = match.replace(' ', '').replace(',', '.')
                    try:
                        amounts.append((float(clean_amount), match))
                    except ValueError:
                        continue
                if amounts:
                    largest_amount = max(amounts, key=lambda x: x[0])
                    return largest_amount[1], 0.6
            
            elif field_type == 'date':
                return self.normalize_date(matches[0]), 0.6
            
            elif field_type in ['provider', 'address']:
                return matches[0], 0.6
        
        return None, 0.0

    def normalize_date(self, date_str: str) -> str:
        """Normalize date to YYYY.MM.DD format"""
        # Remove extra spaces and normalize separators
        date_str = date_str.strip().replace('-', '.').replace('/', '.')
        
        # Ensure we have YYYY.MM.DD format
        parts = date_str.split('.')
        if len(parts) == 3:
            year, month, day = parts
            return f"{year.zfill(4)}.{month.zfill(2)}.{day.zfill(2)}"
        
        return date_str

    def extract_bill_info(self, pdf_path: str) -> Dict[str, Any]:
        """Extract all bill information from a PDF file"""
        filename = os.path.basename(pdf_path)
        self.logger.info(f"Processing: {filename}")
        
        # Initialize result structure
        result = {
            'fájlnév': filename,
            'összeg': 'NOT_FOUND',
            'pénznem': 'Ft',
            'számla_kelte': 'NOT_FOUND',
            'szolgáltató': 'NOT_FOUND',
            'fogyasztó_címe': 'NOT_FOUND',
            'feldolgozási_státusz': 'SIKERES',
            'bizonytalanság_flag': 'NEM'
        }
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            result['feldolgozási_státusz'] = 'HIBA: Szöveg kinyerés sikertelen'
            self.logger.error(f"Failed to extract text from {filename}")
            return result
        
        # Extract each field
        fields_to_extract = ['amount', 'date', 'provider', 'address']
        field_mapping = {
            'amount': 'összeg',
            'date': 'számla_kelte', 
            'provider': 'szolgáltató',
            'address': 'fogyasztó_címe'
        }
        
        uncertain_fields = []
        
        for field_type in fields_to_extract:
            # Try keyword-based extraction first
            value, confidence = self.find_field_by_keywords(text, field_type)
            
            # Fallback to pattern matching if needed
            if not value or confidence < 0.8:
                fallback_value, fallback_confidence = self.extract_by_patterns(text, field_type)
                if fallback_value and fallback_confidence > confidence:
                    value, confidence = fallback_value, fallback_confidence
            
            # Store result
            result_key = field_mapping[field_type]
            if value:
                result[result_key] = value
                if confidence < 0.8:
                    uncertain_fields.append(result_key)
                    self.logger.warning(f"Uncertain extraction for {field_type} in {filename}: {value} (confidence: {confidence:.2f})")
            else:
                self.logger.warning(f"Could not extract {field_type} from {filename}")
        
        # Set uncertainty flag
        if uncertain_fields:
            result['bizonytalanság_flag'] = 'IGEN: ' + ', '.join(uncertain_fields)
        
        return result

    def process_directory(self, input_dir: str, output_csv: str = 'számla_összesítő.csv') -> None:
        """Process all PDF files in directory and export to CSV"""
        if not os.path.exists(input_dir):
            self.logger.error(f"Input directory does not exist: {input_dir}")
            return
        
        # Find all PDF files
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {input_dir}")
            return
        
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF file
        results = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            try:
                result = self.extract_bill_info(pdf_path)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing {pdf_file}: {str(e)}")
                # Add error result
                error_result = {
                    'fájlnév': pdf_file,
                    'összeg': 'NOT_FOUND',
                    'pénznem': 'Ft',
                    'számla_kelte': 'NOT_FOUND', 
                    'szolgáltató': 'NOT_FOUND',
                    'fogyasztó_címe': 'NOT_FOUND',
                    'feldolgozási_státusz': f'HIBA: {str(e)}',
                    'bizonytalanság_flag': 'NEM'
                }
                results.append(error_result)
        
        # Export to CSV
        self.export_to_csv(results, output_csv)
        
        # Summary
        successful = len([r for r in results if r['feldolgozási_státusz'] == 'SIKERES'])
        uncertain = len([r for r in results if r['bizonytalanság_flag'].startswith('IGEN')])
        
        self.logger.info(f"Processing complete. {successful}/{len(results)} files processed successfully.")
        if uncertain > 0:
            self.logger.info(f"{uncertain} files have uncertain extractions and need human review.")

    def export_to_csv(self, results: List[Dict], output_path: str) -> None:
        """Export results to CSV with Hungarian headers and semicolon separator"""
        if not results:
            self.logger.warning("No results to export")
            return
        
        headers = ['fájlnév', 'összeg', 'pénznem', 'számla_kelte', 'szolgáltató', 'fogyasztó_címe', 'feldolgozási_státusz', 'bizonytalanság_flag']
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
                writer.writeheader()
                writer.writerows(results)
            
            self.logger.info(f"Results exported to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {str(e)}")

def main():
    """Main function to run the bill extractor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract information from Hungarian utility bills')
    parser.add_argument('input_dir', help='Directory containing PDF files')
    parser.add_argument('-o', '--output', default='számla_összesítő.csv', help='Output CSV file name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    extractor = BillExtractor(log_level=log_level)
    
    extractor.process_directory(args.input_dir, args.output)

if __name__ == "__main__":
    main()
