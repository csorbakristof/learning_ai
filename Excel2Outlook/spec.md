# Overview

This solution contains several Excel macros (VBA scripts) which control Outlook (sending emails and analysing responses) based on the data retrieved from Excel tables.

In this description every feature (typically subsections of this description) have a code name in brackets like "[F01]". Use these code names to refer to the features.

# [SingleSend] Single sending emails

Input: a single worksheet in Excel which contains email addresses and further columns with text which have to be substituted into email templates. This worksheet will be referred to as "UserList", but its name in Excel may be different. It is always the current worksheet the macro is started from. Another worksheet called "EmailTemplate" contains the template for an email in the upper-left cell (always cell A1).

The macro is started by Ctrl-Shift-D (standing for Drafting). If the user starts the macro, the macro checks the row the cursor is located in. It opens a new email in Outlook and writes its metadata and text body based on the data in that current row. It does not send the email, that is left to the user after reviewing the text.

The "To" field of the email is taken from the "email" column in the current row. "Subject" is taken from the Subject column. 

The body of the email is created from the template mentioned above. It may contain placeholders like "[Name]" (it may contain spaces and it is case sensitive, always in square brackets). These are substituted with values taken from the UserList worksheets column with the same title as the placeholder. Column titles are case sensitive and always in row 1 and always look for exact title matches between columns and placeholders.

If the UserList worksheet contains a FileToAttach column and the value for a given row is not empty, the file with that name (located beside the current excel file in the same directory) should be attached to the email. 

## Further details

- If any column needed by the macro is missing, an error message has to be shown and the process should stop.
- If Outlook is not available, show an error message and stop.
- Preserve the formatting and line breaks of the template. It is only plain text now with line breaks.
- Missing placeholder values (both in case of non-existing column or empty cell) should issue an error message and stop the macro.
- When creating the email, it should be a draft which is shown in the compose window but not sent yet.
- If Outlook is not running, start it.
- Add code to register the shortcut for the macro. It should run when the workbook is opened.
- If the EmailTemplate worksheet does not exist, show an error message.
- Error messages should be detailed so the user has guidance how to fix the issue.

## Details about file attachment

- The name of the "FileToAttach" column (case sensitive check) should also be stored in a constant in the source code.
- Support relative path with the filenames. Base directory for the relative path should be the directory where the excel file is saved.
- If there is an error with attaching a file, MassiveSend should be interrupted and no emails should be drafted. Just like in the case of other validation errors.
- You do not need to support attachment of multiple files.
- You do not need to apply any validation for the files.
- File attachment is an optional feature. If the FileToAttach column does not exist of the corresponding cell is empty, simply do not attach anything. No warning or error message should be issued in this case.


# [MassiveSend] Massive sending emails

This function is another macro which sends emails just like the SingleSend feature, but it sends individual emails for every row in the UserList worksheet.

## Further details

- Take all visible rows into account. The user may use filtering to select a set of rows.
- If there is an error with one of the rows, stop, show an error message and do not draft any emails.
- The MassiveSend feature should be triggered by Ctrl-Shift-M.
- Only create the email drafs bulk but do not send them.
- Do not show progress, only a summary at the end.
- If there are more than 20 emails to create, ask for user confirmation whether to proceed.

# [ResponseCollector] Response collection from answers on an email

# Later features (not to be implemented now)

- Default values for the columns in Excel (upwards firs non-empty cell value)
- Option to send to a set of users (multiple rows based on filtering or selection), they can get it as a single email with multiple addressees (only if other data are the same), everyone in bcc, or individual emails for everyone.

