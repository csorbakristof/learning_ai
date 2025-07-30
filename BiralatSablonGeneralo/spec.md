# Overview

(In this description, software features may have code names shown in brackets like "(INITLIST)". AI tools should use these code names when referring to the feature.)

This project is a set of Excel macros aiming to generate template documents for BSc and MSc thesis reviews. The macros take an external Excel file (exported from the departments portal) to insert some data into the generated templates.

The macro InitStudet list opens an Excel file located beside (in the same folder as) the current one and copies all students name, Neptun code, curriculum ("Mérnökinformatikus", "Villamosmérnök" or "Mechatronikai mérnök") and thesis level ("Szakdolgozat" or "Diplomaterv").

After this macro is executed, the Excel file can be saved and sent to colleagues in the department to be used. They only need to mark the students they review in the table and the generator macro creates the templates for all marked students, with the information above already filled in.

The prefilled review Word document has also a macro which exports the document in 3 PDF files: two for uploading to the thesis portal and one to be printed.

# (INITLIST) InitStudent macro

The macro creates a new worksheet (if it exists, it clears its content) called "StudentData".

This macro opens an open file dialog and ask the user to choose another Excel file containing the student data (at the departments portal it is referred to as the "Terhelés" table).

The macro opens this file and from its second worksheet (title contains the work "konzultáció") it copies the columns with header "Tárgy", "Tárgy nept", "Hallgató neve" and "Hallg. nept" into the worksheet "StudentData". It adds an additional empty column with header "Kiválasztva".

This macro is started by the shortcut: Ctrl-Shift-I

# (GENDOCX) TemplateGenerator macro

This macro is started by the shortcut: Ctrl-Shift-G

This macro performs the following steps for all rows in "StudentData" where the cell in the "Kiválasztva" column is not empty. In this section the data in the current row are referenced as "student data".

## Copy and open word document

Copies the Word document "ReviewAndGradeTemplate.docx" located beside the current Excel file the macro is running in. The new name is "Review_" followed by the name of the student ("Hallgató neve" in the student data).

The application opens the document in Word.

## Replace placeholders

It replaces all occurrences of the following placeholders with the texts given below.

- Placeholder "<<SzakdolgozatDiplomaterv>>" is replaced with
    - "Szakdolgozat" if the column "Tárgy" in student data contains "Szakdolgozat" as substring. 
    - "Diplomaterv" if the column "Tárgy" in student data contains "Diplomaterv" as substring.
-  Placeholder "<<StudentName>>" with the content of the column "Hallgató neve" in student data.
-  Placeholder "<<Szak>>" with
    - "mérnökinformatikus" if column "Tárgy" in student data contains the substring "Info",
    - "villamosmérnök" if column "Tárgy" in student data contains the substring "Vill",
    - "mechatronikus mérnök" if column "Tárgy" in student data contains the substring "Mecha".
- Placeholder <<cím>> with the content of the column "Téma címe" in the student data.
- Placeholder <<dátum>> with the current date in format like "2025. június 13.".
       
## Save file

Saves the Word document and closes it.

# (GENPDF) Word macro for PDF export

The word document consists of two parts: the review and the grade. The review part consists of all except the last page. The grade part is the last page.

The macro in the Word file should export 3 PDF files as follows:

- (PDF_REV) The review file to be uploaded to the thesis portal. This contains only the review part (all pages except the last).
- (PDF_GRADE) The suggested grade file is also to be uploaded to the thesis portal. It contains the grade part (only the last page of the document).
- (PDF_PRN) The file to be printed. This contains the review part twice after each other, followed by the grade part once. 

## Double-sided printing logic for PDF_PRN:

The print PDF is designed for double-sided printing where each copy of the review should be printed on separate physical sheets. The structure is:

1. **First copy of review part** (all review pages)
2. **Empty page** (if review has odd number of pages, to ensure proper sheet alignment)
3. **Second copy of review part** (all review pages)  
4. **Empty page** (if review has odd number of pages, to ensure proper sheet alignment)
5. **Grade part** (single page)

**Examples:**
- For 1-page review: Pages 1, 2(empty), 3, 4(empty), 5(grade) = 3 physical sheets
- For 2-page review: Pages 1-2, 3-4, 5(grade) = 3 physical sheets  
- For 3-page review: Pages 1-3, 4(empty), 5-7, 8(empty), 9(grade) = 5 physical sheets

This ensures that when printed double-sided, each review copy occupies complete physical sheets and the grade is on a separate sheet.

This macro is started by the shortcut: Ctrl-Shift-P
