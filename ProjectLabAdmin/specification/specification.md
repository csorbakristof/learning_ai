# Overview

We are automating the creation of project laboratory presentation sessions in a web environment.

Project laboratory presentation sessions (sessions in the followings) are 2 hour long time slots where a given number (usually 9) students can register and present their work. According to the number of students enrolled into the course and the type of their topics we need several kind of thematic presentation sessions.

For the planning of the schedule, the Data collector application fetches student numbers and topic types from the web and creates an Excel table where the user can fill in a table. This table contains multiple time slots for multiple rooms during a week. Usually time slots are 8:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00. Rooms have identifiers, typically QB203, QBF14, and QBF15. In every slot, there can be a session in every room. The session type can be one of the following:

- Software session (codename: SW)
- Hardware and software session (codename: HW)
- English course presentation for foreign students (codename: ENG)
- Generic session for all types (codename: GEN)
- Online generic session (codename: ONLINE)
- Spare time slot for later use  (codename: SPARE)
- Not used timeslot (codename: NONE)

We have to allow for special thematic sessions as well with other given code names (codaname ROBONAUT and AI for example).

When the user fills in the table, the Web Automator application takes it as input and creates the sessions in a web portal. This means filling out a form for every session and pressing a button. The application should fill in the form but wait for the user to press the button to make it safe.

In this description, headings may contain feature IDs in brackets like "(DLXLS)". Use these feature IDs for referencing them and assign IDs when creating new features. If unsure about the suitable ID, just use a numbered one like "(F001)".

# Data collector application

This application creates an Excel file and filles it based on data retrieved from the Internet by downloading and parsing several web pages. In some cases it may need to use Selenium to simulate the actions of a user. 

## (DLXLS) Project topic data collection

On one hand students enrolled to the project laboratory courses choose a topic. There is a downloadable Excel file which contains all student names and the category of their topic.

The Excel file can be downloaded after logging in to the portal www.aut.bme.hu via the URL https://www.aut.bme.hu/StaffMembers/MyWorkload.aspx
and then clicking on the link named "Terhelés exportálása".

The Excel file contains two worksheets, we use the 2nd one containing "konzultáció" in its title. It contains a big table and after the last line, some merged cells containing something like "© BME - Automatizálási és Alkalmazott Informatikai Tanszék" which is not useful now.

## (DLNEP) Student data collection from the Neptun system

To access the Neptun system, go to https://neptun.bme.hu/oktatoi/login.aspx and wait for the user to log in.

Then go to the page https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902 to access the list of courses.

### Finding the course list

In this page there are several html tables so the application has to find the course list table itself.

Hints for finding the correct table:

- The course list table has the following headings among others: Tárgykód, Tárgy név, Követelmény, Tárgy kredit, Oktatók, Kijelölés
- The value in the column "Tárgykód" always starts with "BMEVI".
- Many rows contain "Évközi jegy" in the column with heading "Követelmény". We will only take these into account.
- The column "Kijelölés" contains checkboxes.
- The column "Oktatók" has to contain "Dr. Csorba Kristóf" in every row, although further text may also be in that cell.

The application should use these conditions to find the course list.

### Proceesing to the course details page

The last element of every row in the course list table is a dropdown menu with a plus sign ("+") icon, its alternate text is "Lehetőségek".

To help the application find this menu, in the HTML source, it has following attributes:

- class="contextcell"
- level='1'
- aria-describedby='contextmenu_help'
- role='menu'
- title='Lehetőségek'
- alt='Lehetőségek'

The cell of the menu does not have content, only onfocus event: "onfocus='A2.HandleClick(event)'" which opens a floating menu. In that menu, one of the menu items is "Jegybeírás" and the application should click on that to proceed to the page of the course details.

After clicking, wait 2 seconds for the course details to load.

### Downloading the student list for the course

In the page of the course details after clicking "Jegybeírás", the application needs to take two steps:

First, look for a "select" html field with id="o_course_mark_gridStudents_ddlPageSize" and select the maximal value (500).

Second, look for a button with alternate text "Exportálás Excel-fájlba" and click on it. This will download the student list of the course in Excel format. The application should download the student list for every course in the list automatically.

## (DLFUSION) Data fusion

In this step the data from DLXLS and DLNEP have to be combined into a single dataset. What we need for every student are the following:

- the list of courses they are enrolled into (there may be multiple ones), we should identify the courses by their course code (Tárgykód, the string starting with BMEVI).
- If the student has a topic according to DLXLS,
    - the supervisors name
    - the category of that topic
    - whether it is a hungarian or english topic. English topics title start with "Z-ENG" prefix, this is how to recognize them.
- If the student is enrolled into an english course. In the name of the Excel files from DLNEP the filename contains this information. It has the format "jegyimport_BMEVIxxxxxx_YY_..." where xxx can be anything and it is part of the course code. YY between the two underscores ("_") is a course type. If it starts with a letter "A", it is an english course. Otherwise it is hungarien.

During this step, only the following course codes ("Tárgykód") should be taken into account:

BMEVIAUAL01, BMEVIAUAL03, BMEVIAUAL04, BMEVIAUAL05, BMEVIAUAT00, BMEVIAUAT01, BMEVIAUA019, BMEVIAUML10, BMEVIAUML11, BMEVIAUML12, BMEVIAUML13, BMEVIAUMT00, BMEVIAUMT01, BMEVIAUMT03, BMEVIAUMT10, BMEVIAUMT11, BMEVIAUMT12, BMEVIAUMT13, BMEVIAUM026, BMEVIAUM027, BMEVIAUM039

If there is no Excel file for one of these courses, show a big warning! All these courses should have hungarian and english course type as well, so 2 Excel files are needed for all of them.

All resulting data should be stored in a JSON format file.

## (MKXLSX) Creating the Excel table for session planning

Using the data of DLFUSION, create an Excel table for session schedule planning.

The Excek table should have two parts: upper part is a planner table where the user will have to enter the session types like "SW" and "HW". And the lower part below it shows some statistics about the required number of sessions per category.

### Planner table

The planner table has columns for every weekday-room pair. Week days range from Monday to Friday and the rooms have the following ID-s: QB203, QBF14, and QBF15. These are the columns, 5x3=15 all together. The rows are the time intervals as mentioned before in the Overview.

### Statistics in the Excel table

Show the following statistics to support the users work. Take only the following courses into account:

BMEVIAUMT00, BMEVIAUMT10, BMEVIAUMT12, BMEVIAUM026, BMEVIAUAL01, BMEVIAUAL03, BMEVIAUAL04, BMEVIAUAL05, BMEVIAUML10, BMEVIAUML12, BMEVIAUML11, BMEVIAUML13, BMEVIAUM039

- For every topic category show the number of students. Also indicate the number of sessions for this category. Assume that 9 students fit into a session. In these statistics, only count the hungarian topics, not the english ones. English topic is a separate category called "ENG", show the number of students in english topics only there.
- For every session type (like SW, HW, ENG etc. mentioned in the Overview) show the number of cells in the Planner table which contain this session type identifier. This should be calculated by Excel using formulas and update immediately after editing the table.

# Web automator application

The second takes the Excel file as input and performs actions on a webpage using selenium. In case of Selenium actions, both applications will have to wait first for the user to login. Please create the necessary environment for the two applications in this folder.