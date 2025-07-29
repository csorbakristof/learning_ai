import re

# Test the fixed pattern logic
def extract_course_info_from_filename(filename: str) -> tuple:
    try:
        # Pattern to match the filename format: jegyimport_BMEVIxxxxxx_YY_
        # Use case-insensitive matching since filenames are in uppercase
        pattern = r'jegyimport_([^_]+)_([^_]+)_'
        match = re.search(pattern, filename, re.IGNORECASE)
        
        if match:
            course_code = match.group(1).upper()
            course_type = match.group(2).upper()
            
            # Verify the course code starts with BMEVI
            if course_code.startswith('BMEVI'):
                is_english = course_type.startswith('A')
                return course_code, is_english
            else:
                print(f"Course code {course_code} doesn't start with BMEVI in filename {filename}")
                return course_code, False
        else:
            print(f"No match found for filename {filename}")
            return "UNKNOWN", False
            
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return "UNKNOWN", False

# Test with various filenames from the output
test_files = [
    'jegyimport_BMEVIAUML10_AL_2024_25_2.xlsx',  # Should be English (AL starts with A)
    'jegyimport_BMEVIAUAL01_L_2024_25_2.xlsx',   # Should be Hungarian (L doesn't start with A)
    'jegyimport_BMEVIAUAL03_AL_2024_25_2.xlsx',  # Should be English (AL starts with A)
    'jegyimport_BMEVIAUA019_A01Gy25t_2024_25_2.xlsx', # Should be English (A01 starts with A)
]

print("Testing fixed pattern:")
for filename in test_files:
    course_code, is_english = extract_course_info_from_filename(filename)
    language = "English" if is_english else "Hungarian"
    print(f"{filename}")
    print(f"  -> Course: {course_code}, Language: {language}")
    print()
