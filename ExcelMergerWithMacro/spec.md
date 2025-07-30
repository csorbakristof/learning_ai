# Overview

The project is about an Excel table merge tool. We have a table with names and choosen numbers. People choose numbers for themselves. We send the XLSX file to everyone via email and ask them to put one or more names with corresponding chosen numbers into it. Then they send it back. This is done in the XLSX files worksheet called "Adatgyujto". It has two columns with header "Név" (Column A) and "Választott szám" (column B).

The XLSX file also contains a worksheet called "Gyujtes" where the contents of the current and several other XLSX files "Adatgyujto" worksheets are merged after each other.

The data collection is done by a VBA macro in the Excel file. By activating it via the hotkey Ctrl-Shift-C ("C" stands for collect), the worksheet "Gyujtes" is populated as described above. The data should be collected from all Excel files in the current directory where the currently open Excel file is also located.

# Added after initial test

Please make sure that if the macro finds the file which was the macro started from, that file should not be processed! And definitely make sure it is not closed during the macro execution.
