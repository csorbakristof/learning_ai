"""
Extraction module for processing Excel files and merging them into a single output file.
"""
import os
import re
from openpyxl import load_workbook, Workbook


def extract_semester_name(cell_value):
    """
    Extract semester name from cell A1.
    Expected format: "2025-2026 ősz" félév - téma osztályzatok
    Returns: 2025-2026 ősz
    """
    if not cell_value:
        return None
    
    # Extract text between quotes
    match = re.search(r'"([^"]+)"', str(cell_value))
    if match:
        return match.group(1)
    
    return None


def is_valid_row(row_data):
    """
    Check if a row should be included in the output.
    Skip rows where Grade or GradedBy is missing or contains only "-"
    """
    grade = row_data.get('Grade', '')
    graded_by = row_data.get('GradedBy', '')
    
    # Convert to string and strip
    grade_str = str(grade).strip() if grade is not None else ''
    graded_by_str = str(graded_by).strip() if graded_by is not None else ''
    
    # Skip if either is empty or just a dash
    if not grade_str or grade_str == '-':
        return False
    if not graded_by_str or graded_by_str == '-':
        return False
    
    return True


def process_excel_file(file_path):
    """
    Extract data from a single Excel file.
    
    Returns:
        List of dictionaries containing extracted data
    """
    try:
        wb = load_workbook(file_path, data_only=True)
        ws = wb.active
        
        # Extract semester name from A1
        semester_name = extract_semester_name(ws['A1'].value)
        if not semester_name:
            print(f"  ⚠ Warning: Could not extract semester name from {file_path}")
            semester_name = "Unknown"
        
        # Table starts at row 4 (header row)
        # We need columns B, C, D, E, F (indices 2, 3, 4, 5, 6)
        data_rows = []
        
        # Start from row 5 (data rows after header)
        for row_idx in range(5, ws.max_row + 1):
            # Check if row is empty (stop at first empty row)
            row_cells = [ws.cell(row_idx, col_idx).value for col_idx in range(2, 7)]
            
            # If all cells are None or empty, stop processing
            if all(cell is None or str(cell).strip() == '' for cell in row_cells):
                break
            
            # Extract data from columns B through F
            row_data = {
                'SemesterName': semester_name,
                'StudentNeptunCode': ws.cell(row_idx, 2).value,  # Column B
                'CourseName': ws.cell(row_idx, 3).value,          # Column C
                'CourseNeptunCode': ws.cell(row_idx, 4).value,    # Column D
                'Grade': ws.cell(row_idx, 5).value,               # Column E
                'GradedBy': ws.cell(row_idx, 6).value             # Column F
            }
            
            # Only add row if it passes validation
            if is_valid_row(row_data):
                data_rows.append(row_data)
        
        wb.close()
        return data_rows
        
    except Exception as e:
        raise Exception(f"Error processing file {file_path}: {e}")


def merge_all_files(downloads_dir, output_dir):
    """
    Process all Excel files in downloads directory and merge into single output file.
    
    Args:
        downloads_dir: Directory containing downloaded Excel files
        output_dir: Directory where output file will be saved
    
    Returns:
        Path to the output file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all Excel files from downloads directory
    excel_files = [f for f in os.listdir(downloads_dir) 
                   if f.endswith(('.xlsx', '.xls')) and os.path.isfile(os.path.join(downloads_dir, f))]
    
    if not excel_files:
        raise Exception(f"No Excel files found in {downloads_dir}")
    
    print(f"\nProcessing {len(excel_files)} Excel files...")
    
    # Collect all data
    all_data = []
    
    for idx, filename in enumerate(excel_files, 1):
        file_path = os.path.join(downloads_dir, filename)
        print(f"Processing file {idx}/{len(excel_files)}: {filename}...", end=" ", flush=True)
        
        try:
            data_rows = process_excel_file(file_path)
            all_data.extend(data_rows)
            print(f"✓ Extracted {len(data_rows)} rows")
        except Exception as e:
            print(f"✗ Error: {e}")
            raise
    
    # Create output workbook
    print(f"\nCreating output file with {len(all_data)} total rows...")
    
    output_wb = Workbook()
    output_ws = output_wb.active
    output_ws.title = "All Semester Stats"
    
    # Write header
    headers = ['SemesterName', 'StudentNeptunCode', 'CourseName', 'CourseNeptunCode', 'Grade', 'GradedBy']
    for col_idx, header in enumerate(headers, 1):
        output_ws.cell(1, col_idx, header)
    
    # Write data rows
    for row_idx, data_row in enumerate(all_data, 2):
        output_ws.cell(row_idx, 1, data_row['SemesterName'])
        output_ws.cell(row_idx, 2, data_row['StudentNeptunCode'])
        output_ws.cell(row_idx, 3, data_row['CourseName'])
        output_ws.cell(row_idx, 4, data_row['CourseNeptunCode'])
        output_ws.cell(row_idx, 5, data_row['Grade'])
        output_ws.cell(row_idx, 6, data_row['GradedBy'])
    
    # Save output file
    output_path = os.path.join(output_dir, "AllSemesterProjectStats.xlsx")
    output_wb.save(output_path)
    output_wb.close()
    
    print(f"✓ Output file saved: {output_path}")
    return output_path


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(script_dir, "downloads")
    output_dir = os.path.join(script_dir, "output")
    
    try:
        merge_all_files(downloads_dir, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
