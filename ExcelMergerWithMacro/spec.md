# Overview

The project is about an Excel table merge tool. We have a table with data that needs to be collected from multiple Excel files. We send Excel files to everyone via email and ask them to put data into the first worksheet of the file. Then they send it back.

The Excel file containing the macro starts with just a single empty worksheet and the VBA macro code. When the macro is executed, this single worksheet becomes the target where data from all other Excel files in the current directory is merged.

The data collection is done by a VBA macro in the Excel file. By activating it via the hotkey Ctrl-Shift-C ("C" stands for collect), the currently active worksheet is populated with merged data from all other Excel files. The data should be collected from all Excel files in the current directory where the macro file is located.

## Data Collection Rules

- The macro should collect data from the **first worksheet** of each Excel file in the directory
- **No assumption** should be made about column numbers or specific headers
- Whatever structure exists in the first worksheet should be copied entirely
- Headers should be copied from the first processed file and used as the reference
- The **currently active worksheet** in the macro file should be **completely cleared** before data collection starts
- If headers in subsequent files **do not match** the reference headers from the first file, an **error message** should be displayed
- An additional column should be added to track the source file name for each record
- The macro file itself should **not be processed** (it starts empty and becomes the target)

# Added after initial test

Please make sure that if the macro finds the file which was the macro started from, that file should not be processed! And definitely make sure it is not closed during the macro execution.
