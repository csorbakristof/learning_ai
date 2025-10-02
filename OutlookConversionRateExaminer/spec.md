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


