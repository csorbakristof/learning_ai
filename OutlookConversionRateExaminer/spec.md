# Overview

This is an Outlook macro based solution to scan for emails sent by a person and their responses from outside the organization.
We plan to use it to measure the conversion rate of contacting companies.

The macro should
- ask for a sender (person given with email address), we will call it SenderPerson
- a domain name (by default, bme.hu), everyone inside this domain is not an external company. Other addresses are.
- Scan for all emails sent by SenderPerson
- Create a collection of emails called "OutgoingEmails" which contains all emails sent by SenderPerson, the text body contains "EDIH" and the recipient is outside the "bme.hu" domain.
- For every email in OutgoingEmails (we will call it OriginalEmail), collect all response emails (called "ResponseEmail") which came from outside "bme.hu".
- Create an Excel Sheet where the first 4 columns contain the original email date, sender, subject, recipient. The 5th column is the number of responses received for the OutgoingEmail of the current row.

## Futher details

- SenderPerson, Domain Name: the macro should ask for the email address and domain name via input boxes.
- Email search scope: look for all mail folders, but check only the last 3 months.
- Responses should be identified based on the Conversation ID.
- The macro should create a new Excel file everytime and keep Excel open so that the user can save it.
- The macro will be run in Outlook Desktop.

# Modification request

Modify the macro so that it only does the following:
- It looks for emails either
    - direction: either "sent" or "received"
    - going to external recipients and the body contains AI EDIH and the cutoff date is OK, or
    - received from external senders
- Put all the found emails into the Excel table with the following columns:
    - Sender email address
    - Recipients email addresses (only in To field, cc and bcc should not be taken into account)
    - Subject
    - Date of sending/receiving the email
    - Conversation ID

This macro (to be run in Outlook desktop) should be in the file ExternalEmailCollector.vba

A second macro (into file EmailResponseCounterInExcel.vba, to be run in Excel desktop) should go along the email list above and for all "sent" emails it should collect the number or "received" emails with the same Conversation ID and put the count into an additional column called "ResponseEmailCount" (this is the title in the header).

## Further details

Outlook macro:

- Whether an email is "sent" or "received" should be decided based on the content of the sender email address.
- The "AI EDIH" criteria only applies to the sent emails. Mentioning "EDIH" is sufficient, "AI" is not necessarily needed.
- The new macros should also ask for the sender email address and the domain of the organization.
- When you check the domain of the email address, make sure not to check exact equality. If the domain name of the email address ends with the given domain name, that is already a match. Any subdomains should be accepted.
- Exclude the cc and bcc recipients entirely.

Excel macro:

- The data can be assumed to be in the first worksheet.
- Count the responses only for the "sent" emails.
- If the Excel table does not have these columns, issue a detailed error message.
- You can assume that the table columns have been created by the Outlook macro and so you can hardwire their location. No need for additional validation.

# Further modification: collect partner email addresses

Extend the Outlook macro so that it creates two worksheets: the content above should go into worksheet "ExternalEmails". Another one should also be created where all external email addresses should be collected from the recipient fields of the sent emails.
It should have two columns: "External email" and "Is EDIH partner". The second column should be filled with default "1" values.

Modify the Excel macro so that it counts the responses only for those "sent" emails which have a recipient in the "External email" column and the "Is EDIH partner" value for them is "1". (Users will set the "Is EDIH partner" value for some email addresses to 0 if that email address does not belong to a true partner and as such, should not be taken into account, although it is an external email address.)
