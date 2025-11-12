# Overview

This solution contains several Excel macros (VBA scripts) which control Excel and Word to generate a set of files using Word template documents and data from the excel file.

In this description every feature (typically subsections of this description) have a code name in brackets like "[F01]". Use these code names to refer to the features.

Everything is controlled by macros in a single Excel file which will be referred to as the "controller" excel file.

# [CollectStudents] Collect students, course codes and advisors

The goal of this feature is to generate most of the content of the worksheet "GeneráltHallgatóiLista". A macro called "CollectStudents" should perform this procedure. It should be triggered by the hotkey Ctrl-Shift-C which is registered when opening the workbook.

## [CollectTerhelesExportData] Collect the data from Terhelés export

Input data are located in another Excel file located in the same directory as the controller excel file. Its name starts with "Terhelés", this can be used to find it. I will refer to this file as "terhelés excel". Inside the terhelés excel, there is a worksheet which has "konzultáció" in its name. (Full name varies so this substring should be searched for.) Populate the columns of GeneráltHallgatóiLista from this "konzultáció" worksheet in "terhelés excel" as follows:

- Hallgató neve: take "Hallgató neve" column from the source
- Neptun kód: take "Hallg. nept" column from the source
- Tárgykód: take "Tárgy nept" from the source
- Dolgozat megnevezése: use a lookup formula "=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:D,2,FALSE),""nincs"")" where you adapt $C2 to the current row.
- Szak megnevezése: use a lookup formula "=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:D,3,FALSE),""nincs"")" where you adapt $C2 to the current row.
- Konzulens neve: take "Konzulens" from the source, but if there is anything in brackets after the name, remove that.
- Konzulens beosztása: leave empty for now

## [CollectZvSegedData] Collecting additional information from "ZV segéd" export

The Excel file "reviewTemplates_reports.xlsx" is another data source which contributes to the data in the GeneráltHallgatóiLista worksheet.

Fill in the following columns of GeneráltHallgatóiLista based on the information in this file. Copy the corresponding values, do not use Excel formulas here. For every row, match the records based on the column "Neptun kód" in GeneráltHallgatóiLista and "Neptun kód" in "reviewTemplates_reports.xlsx". If there is no match, leave the fields empty. You can assume that the following columns already exist.

- "Dolgozat címe magyarul": copy from column "Téma címe"
- "Dolgozat címe angolul": copy from column "Téma angol címe"
- "Bírálat nyelve": set it to "angol" if column "Külföldi" contains the exact text "True", and set it to "magyar" in every other case (different content, empty field etc.).

## [CleanUpList] Clean up the list

Remove all rows from "GeneráltHallgatóiLista" where the column "Dolgozat megnevezése" is either empty, contains "0" or "nincs", or column "Dolgozat címe magyarul" is empty.

In this function, when locating the last row of the worksheet, take all columns into account as some rows have only values in a few columns and they have to be removed as well.

## Further details

- The template documents and input excel files are located beside the controller Excel file.
- Save the output documents into a subdirectory with the name of the advisor ("Konzulens neve") which is made filesystem friendly.
- Clear GeneráltHallgatóiLista before populating it.
- You can assume that worksheet headers are already present in row 1 in all Excel files and worksheets.
- In case any error occures, show a detailed error message so that the user knows how to fix it and stop the procedure.
- Use worksheet and column header names for identifying them.
- No data validation is required.
- Close all Excel files except the controller one after processing.
- Filesystem friendly strings: use the following method to convert any string (like student name) to be filesystem friendly. Remove whitespaces and convert accents and special characters to english letters. Use PascalCasing, so for example "Csorba Kristóf" should be converted to "CsorbaKristof".
- If any of the mentioned Excel files or worksheets inside them is missing, show a detailed error message and stop the macro.

# [GenerateDocuments] Generate the documents

This feature is a separate macro called GenerateDocuments and should be triggered by Ctrl-Shift-G. It goes along every row in "GeneráltHallgatóiLista" and creates several Word documents using the data in the row and Word documents as template documents.

If any value of "GeneráltHallgatóiLista" required for the generation of a document is missing, show an error message and stop. Check only for the presence of columns actually used.

## Templates for the document generation

For every row of "GeneráltHallgatóiLista", the macro should go along the rows (except header) of the worksheet "TemplatesAndFiles". Every row of this sheet corresponds to a Word document to create. If any of the columns mentioned below is missing, show an error message and stop.

The column "Kimeneti fájl sablon" contains the name template of the output file. For the input template, use "Angol sablon" if "Bírálat nyelve" in "GeneráltHallgatóiLista" is "angol", use "Magyar sablon" in every other case. (These are the exact column names.) The filename templates are strings containing "name" which should be substituted by the student's name (made filesystem friendly). The student name is found in the column "Hallgató neve" in "GeneráltHallgatóiLista".

## Filling out the templates

Everytime the macro generates a document based on a template, it should open the template, substitute placeholders, save the file, and close Microsoft Word.

Placeholders are texts in brackets like "[xyz]" found in the template documents. The "xyz" is the name of the placeholder. Every placeholder should be substituted by the value in "GeneráltHallgatóiLista" where the column matches exactly the placeholder's name. So for example the placeholer "[Bírálat nyelve]" should be replaced with the value in the column "StudentName" of the current student's row in "GeneráltHallgatóiLista".

There are special placeholders:
- The placeholder "[date]", insert a Word field which always updates to the current date.

## Further details

- If the output directory does not exist, create it.
- If a word document already exists, overwrite it.
- String replacement should happen case sensitive and globally as we can be sure there will be only a single match.
- If the word template file does not exist, issue an error.
- Start Microsoft Word if needed and at the end, close it.
- If there is an error, show a detailed error message and stop the processing of further rows.
- Show progress indication as this procedure may take a long time. Use the status bar in excel.
- At the end, show a report what has been done and whether there were errors.
- Word does not need to be visible.
