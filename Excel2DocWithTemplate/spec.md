# Overview

The goal of this project to generate PDF files based on mutiple templates and data from Excel sheets.

The ControllerSheet.xlsm contains the data in its "Data" worksheet in columns A to C.

In columns E to F there are Word template filenames in row 1.

Some functions are created by macros in the Excel table. After they are executed, the hotkey Ctrl-Shift-G is created. It starts a macro which generates a new document file in the output folder.
The output document depends on the cell where the hotkey is pressed. It generates the document based on data in the current row and the template file mentioned in row 1 of the current column.

For example if the hotkey is pressed in cell E3, it will create a document in the following way:
- The documents name is the concatenation of the value "Név" (in this case, content of cell A3 as "Név" is the header or column A), and the template filename in cell E1 which is "MsgTemplate.docx" in this case. So the output is written to the file "Nóri_MsgTemplate.docx".
- In the document template, placeholders for dynamic values have the form "<<Név>>" in which case the value substituted there is the value in column "Név" (cell A3 in this example).




