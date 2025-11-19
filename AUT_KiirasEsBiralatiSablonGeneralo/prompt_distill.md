# VBA Implementation Prompt - AUT Kiírás És Bírálati Sablon Generáló

## Context
Implement Excel VBA macros for generating Word documents from templates based on student data collected from multiple Excel sources.

## Requirements

### Module Structure
Create a VBA module file `BiralatGeneralo.vba` with the following features:

---

## Feature 1: [CollectStudents] - Collect Students Data

**Trigger:** Ctrl+Shift+C (register in ThisWorkbook.Workbook_Open event)

**Purpose:** Populate the "GeneráltHallgatóiLista" worksheet from multiple data sources.

### Sub-feature: [CollectTerhelesExportData]

**Input:** Excel file starting with "Terhelés" in the same directory
- Find worksheet containing "konzultáció" in its name
- Copy data to "GeneráltHallgatóiLista":
  - Hallgató neve ← "Hallgató neve"
  - Neptun kód ← "Hallg. nept"
  - Tárgykód ← "Tárgy nept"
  - Dolgozat megnevezése ← `=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:F,2,FALSE),"nincs")`
  - Szak megnevezése ← `=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:F,3,FALSE),"nincs")`
  - Konzulens neve ← "Konzulens" (remove text in brackets)
  - Degree level ← `=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:F,4,FALSE),"nincs")`
  - Program name ← `=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:F,5,FALSE),"nincs")`

### Sub-feature: [CollectZvSegedData]

**Input:** File "reviewTemplates_reports.xlsx" in same directory
- Match rows by "Neptun kód" column
- Copy values (not formulas):
  - Dolgozat címe magyarul ← "Téma címe"
  - Dolgozat címe angolul ← "Téma angol címe"
  - Bírálat nyelve ← "angol" if "Külföldi" = "True", else "magyar"

### Sub-feature: [CleanUpList]

Remove rows where:
- "Dolgozat megnevezése" is empty, "0", or "nincs" (case-insensitive)
- OR "Dolgozat címe magyarul" is empty

Use `UsedRange` to find last row (account for all columns).

### Implementation Details:
- Clear "GeneráltHallgatóiLista" before populating (keep header row)
- Use column header names for identification (via `GetColumnNumber` helper)
- Close all opened Excel files after processing
- Show detailed error messages and stop on error
- Headers are in row 1 of all worksheets

---

## Feature 2: [GenerateDocuments] - Generate Word Documents

**Trigger:** Ctrl+Shift+G (register in ThisWorkbook.Workbook_Open event)

**Purpose:** Generate Word documents from templates for each student.

### Process Flow:
1. Create new Word instance (not visible)
2. For each row in "GeneráltHallgatóiLista":
   - Get student name, advisor name, review language
   - Create output directory: `{WorkbookPath}\{FilesystemFriendlyAdvisorName}`
   - For each row in "TemplatesAndFiles":
     - Select template: "Angol sablon" if language="angol", else "Magyar sablon"
     - Generate output filename: replace "name" with filesystem-friendly student name
     - Open template, replace placeholders, save, close document
3. Close Word instance
4. Show summary report

### Placeholder Replacement:
- Find all `[xyz]` patterns in document
- Match placeholder name with column headers (case-insensitive)
- Replace with cell value from current student's row
- Replacement is case-insensitive but original case preserved

### Validation:
- Check that all placeholders in document have corresponding columns
- Check that required values exist (student name, advisor name, placeholder values)
- Stop entirely on error with detailed message

### Implementation Details:
- Show progress in Excel status bar: "Dokumentumok generálása: X/Y hallgató..."
- Create output directories if needed
- Overwrite existing files
- Dynamic placeholder detection (scan document for `[xxx]` patterns)
- Two-pass approach:
  1. Check for missing columns and values
  2. Replace all placeholders
- Report: processed count, errors if any

---

## Helper Functions

### `ClearGeneraltHallgatoiLista()`
Clear rows 2+ keeping row 1 headers.

### `FindFileStartingWith(folderPath, prefix)`
Find first file matching pattern `{prefix}*.xls*`.

### `FindWorksheetContaining(wb, searchText)`
Find worksheet with `searchText` in name (case-insensitive).

### `GetColumnNumber(ws, headerName)`
Find column number by header name in row 1. Raise error if not found.

### `MakeFilesystemFriendly(inputStr)`
Convert to PascalCase, replace Hungarian accents:
- á→a, é→e, í→i, ó→o, ö→o, ő→o, ú→u, ü→u, ű→u (both cases)
- Remove spaces, hyphens, underscores
- Example: "Csorba Kristóf" → "CsorbaKristof"

### `GenerateSingleDocument(wordApp, studentWs, studentRow, templateFile, outputFile)`
- Open template document
- Create Dictionary for placeholders (case-insensitive mode)
- First pass: Find placeholders in document, validate columns exist and values not empty
- Call `CheckForUnknownPlaceholders` to validate all placeholders
- Second pass: Replace all placeholders with values
- Save and close document

### `CheckForUnknownPlaceholders(wordDoc, studentWs, templateFile)`
- Scan document text for all `[xxx]` patterns
- Check each placeholder against worksheet columns (case-insensitive)
- Raise error if any placeholder doesn't have matching column
- Error message includes: list of unknown placeholders, template file path

---

## Error Handling

**All errors must:**
- Show detailed messages with context (file names, row numbers, column names)
- Stop macro execution immediately
- Close any opened files/applications

**Specific error cases:**
- Missing Excel files or worksheets
- Missing columns in worksheets
- Empty required values (student name, advisor name, placeholder values)
- Missing template files
- Placeholders without corresponding columns

---

## ThisWorkbook Module Code

```vba
Private Sub Workbook_Open()
    Application.OnKey "^+C", "CollectStudents"
    Application.OnKey "^+G", "GenerateDocuments"
End Sub
```

---

## Technical Notes

- **Do NOT** include `Attribute VB_Name` in the .vba file
- Use `Option Explicit`
- All worksheets must have headers in row 1
- Template files are Word documents (.docx)
- Word automation uses late binding (CreateObject)
- Progress indication via `Application.StatusBar`
- Reset status bar with `Application.StatusBar = False`
- VLOOKUP formulas reference 'Tantárgyi adatos' worksheet range B:F
- Dictionary CompareMode = 1 for case-insensitive key matching
- Word Find MatchCase = False for case-insensitive placeholder matching
