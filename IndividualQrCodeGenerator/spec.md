# Individual QR code generator

I want to have a html+javascript page which can generate QR codes for me so I can show them to my students. All students get an individual QR code, so I need a button to simply generate the next one.

The QR codes contain an URL pointing to a Google Forms form and the URL contains the prefilled value of some fields in the form. They are:

- A topic string which helps to categorize the answers provided in the Google Forms form. It is a short name or text of any kind. It may contain special characters.
- A random ID which is a random number between 1 and 10000.
- A timestamp.(Date, hours, minutes, seconds)
- A validation code.

The validation code is the first 5 characters of an SHA1 hash code of the following:

- The random ID
- The timestamp
- A salt value (hardwired into the html+javascript code, arbitrary string even with special characters).

For cases when the student is unable to use the QT code, the contained values should be displayed below the QR code.

# Generator page

I need a html+javascript based page which can generate the above HTML page for me (for downloading) if I tell it in a simple html form:

- the Google Forms URL
- the salt value
- the parameter name of the Google Form fields of topic, random ID and timestamp to be used in the querystring.

## Clarification details:

- I want to use the specific Google Forms Pre-filled URL format where each field has a unique entry.xxxx ID. The user will set these entry IDs in the setup form.
- The validation code should also be passed as a URL parameter to the Google Form, so that it is included in the answers.
- Timestamp Format: YYYYMMDDHHMMSS. It should contain the time the Generate button was clicked.
- Security Context: It is OK to have the salt "hardwired" into the client-side JavaScript, the only place it will be stored at is my phone.
- I want you to generate a single html+javascript file, the generator page. It should generate a single, standalone HTML file with everything embedded into it, ready for download.

# Validation page

I need a separate html+javascript page where I can copy-paste the content of the Google Form answers (from Google Sheets directly), set the salt, and then it validates all rows whether validation code is correct, and the fill-on timestamp and the timestamp in the QR code has a time difference not more than 10 minutes.

This should also be a single html file you generate for me.
