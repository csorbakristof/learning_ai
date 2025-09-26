# Overview

This solution contains several Excel macros (VBA scripts) which control Excel and Word to generate a set of files using a Word template document and data from the excel file.

In this description every feature (typically subsections of this description) have a code name in brackets like "[F01]". Use these code names to refer to the features.

Everything is controlled by macros in a single Excel file which will be referred to as the "controller" excel file.

# [CollectStudents] Collect students, course codes and advisors

The goal of this feature is to generate most of the content of the worksheet "GeneráltHallgatóiLista". Input data are located in another Excel file located in the same directory as the controller excel file. Its name starts with "Terhelés", this can be used to find it. I will refer to this file as "terhelés excel". Inside the terhelés excel, there is a worksheet which has "konzultáció" in its name. (Full name varies so this substring should be searched for.)

Populate the columns of GeneráltHallgatóiLista from this "konzultáció" worksheet in "terhelés excel" as follows:

- Hallgató neve: take "Hallgató neve" column from the source
- Neptun kód: take "Hallg. nept" column from the source
- Tárgykód: take "Tárgy nept" from the source
- Dolgozat megnevezése: use a lookup formula "=IFERROR(VLOOKUP($C2,'Tantárgyi adatok'!B:D,2,FALSE),""nincs"")" where you adapt $C2 to the current row and column C.
- Szak megnevezése: similarly to "Dolgozat megnevezése", but this time take the value from the column D ("Szak megnevezése") in the worksheet "Tantárgyi adatok". Here you may also use a lookup formula in Excel.
- Konzulens neve: take "Konzulens" from the source
- Konzulens beosztása: leave empty for now
- Feladatkiírás fájlnév: set it to "kiirasok/xxxxxx.docx" where you substitute xxxxxx with the student name (column "Hallgató neve"). You can use an Excel formula to do this.

A macro called "CollectStudents" should perform this procedure. It should be triggered by the hotkey Ctrl-Shift-C which is registered when opening the workbook.

## Further details

- Clear GeneráltHallgatóiLista before populating it.
- You can assume that worksheet headers are already present in row 1.
- In case any error occures, show a detailed error message so that the user knows how to fix it and stop the procedure.
- Use worksheet and column header names for identifying them.
- No data validation is required.
- Close "terhelés excel" after retrieving the data.
- In the column "Feladatkiírás fájlnév", clean up the student name for file system compatilibity: remove whitespaces and convert accents and special characters to english letters.
- For the lookup columns use the formulat "=XKERES($C2;'Tantárgyi adatok'!B:B;'Tantárgyi adatok'!C:C;"nincs")"

# [GenerateTaskDescriptions] Generate task descriptions

This feature is a separate macro called GenerateTaskDescriptions and should be triggered by Ctrl-Shift-G. It goes along every row in "GeneráltHallgatóiLista" and creates a Word document using the data in the row and a Word template document.

If the row has the values "nincs" or "0" in the column "Dolgozat megnevezése" or "Szak megnevezése", skip that row and do not generate a file for it.

The template document is located beside the controller Excel file with the name "FeladatkiirasSablonAUT.docx" (store this name in a constant). For every row open this document, apply the following changes and save it with the filename in the column "Feladatkiírás fájlnév".

The changes to apply to the template document:

- There are two dropdown lists. In the first, choose the value matching the column "Dolgozat megnevezése". In the second dropdown list, choose the value from "Szak megnevezése".

- Replace "Dr. Érték Elek" with the value in column "Konzulens neve".
- Replace the string "Budapest, 2020. szeptember 4." at the end of the document with "Budapest, " and the current date in hungarian format like "2025. szeptember 26.".

Save the file and proceed to the next row.
