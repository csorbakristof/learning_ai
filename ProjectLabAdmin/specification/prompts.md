# Initial prompt

We are going to create two python console applications: the first creates an Excel file and filles it based on data retrieved from the Internet by downloading and parsing several web pages. In some cases it may need to use Selenium to simulate the actions of a user. The second takes the Excel file as input and performs actions on a webpage using selenium. In case of Selenium actions, both applications will have to wait first for the user to login. Please create the necessary environment for the two applications in this folder.

---

Have a look at @specification.md and implement the feature DLXLSX.

---

Let's test the DLXLS feature.

---

Now proceed to the DLNEP feature and implement it.

----

In the followings, whenever I start a prompt with "Q:", just answer my question without taking any action or editing code.

---

Q: can we start the DLNEP feature without starting the DLXLS feature?

----

Then please start DLNEP for testing.

---

I have interrupted the process, sorry. It seems there are lots of tables in that page beside the course list. You can find the course list table with the following hint: every row has to contain the text "Dr. Csorba Kristóf" in one of the cells, although further text may be in that cell as well. This condition is probably true only for one of the tables, the course table itself. Add this filtering hint to the code please.

----

Further more, every row of the course list starts with the cell containing the course code which always starts with "BMEVIAU". Use that hint too.

----

Sorry, course code prefix check should look for "BMEVI", the remaining part may differ sometimes.

----

I have updated the conditions and hints for finding the couse list table in @specification.md, so please have a look at that and update the code accordingly.

---

I have interrupted the process. I have updated the @specification.md to further help to find the "Jegybeírás" menu item. Please update the code according to this.

---

OK, lets find the issue. And please not that Neptun needs time to load course details, waiting 2 seconds may not be enough. Make that 5 seconds for now.

---

I have updated @specification.md
On one hand it is enough to wait 2 seconds after clicking on "Jegybeírás", and on the other hand, I added to change a selector (dropdown list) before clicking on "Exportálás Excel-fájlba" as sometimes it is needed to avoid an unexpected popup question. Please update the code accordingly.

----

DLNEP seems to work fine. A little bit slow. Please update the "time.sleep(5)" waitings to 2 seconds, that is enough for the pages to load everywhere.

-----

Have a look at @specification.md and implement the feature DLFUSION so that if DLXLS and DLNEP have were already executed, I do not need to rerun them, just use the downloaded files. Do you need help with combining the data from those Excel files according to the specification?

---

Please run DLFUSION.

---

I have updated the specification of MKXLSX, start to implement it.

----

Please update the @QUICK_START.md file and all implementation description files according to the current code base. If it is of help, create an InformationForAI.md file which describes the solution for AI agents who need to catch up. This file should accelerate the initial phase of development so that the structure does not have to be inferred by reading the whole source code.

---

I extended the @specification.md at DLFUSION and MKXLSX to separate english courses from the hungarian ones. Please read it and start to update DLFUSION first.

----

Now proceed to the update of MKXLSX.

----

Q: The DLXLS feature seems to start over after downloading all Excel files. After finishing, it started to download the first course again. Can you please check whether this is true?

---

I have extended DLFUSION in @specification.md to use a given list of course codes. Please update the code.

---

Now the course code filtering is also influencing the MKXLSX feature. Update that too, please.

---

Please have a look at the overall source code. Some files seem to be very long. Please refactor according to the SOLID principles to get a maintainable code.

---

Remove all downloaded files and fresh start the whole system for a complete test.

# Topic collector

Hello! I need you to create an additional python+selenium application which is independent from the previous ones. Put it in a folder called app3_topic_collector. Look at the specification in @specification_topiccollector.md . Can you generate the application for me? Ask me if you need additional information.

---

Yes, please run the application so I can see the resulting JSON.

---

The app seems to open the pages of advisors as well which is not required. Advisors appear in the details pages of the topics but we only need their names, so clicking on their name (it is also a link) is not necessary. Why is the application doing that?

(A kategória oldalon minden linket megvizsgált, pedig a témák után szerepel a konzulensek neve is és az is link. Azt nem kellene követni...)

---

Ahhhh.... I see the issue! You need to login to the portal to see the selectors. Please modify the application to open the website and then wait for the user to log in before continuing.

## Drop selector clicking and selenium and login at all

I realized that we can solve the whole task much easier and faster: the list of course codes appears on the category pages, so the app can extact them from there for every topic which is contained in that category. And then there is no need for the selector manipulation at all. Which also means that there is no need to login and no need for selenium at all. We can solve this with simple static html downloads. Please modify the @specification_topiccollector.md file accordingly.

----

Now please modify the code according to the new specification.

---


# Tanulságok

Pontos körbeírás alapján megtalálta a Neptun oldalon azt, amire klikkelni kellett. De az a biztos, ha sok szűrőfeltétel van (mert TABLE igen sok volt az oldalon) és még jobb, ha pl. element id-t meg tudok neki mondani.

Ha egy xlsx tartalma kell neki a munkához, simán kiíratja a terminálra egy python scripttel és ezzel gyakorlatilag megnézi, min van a fájlban, megnézi, milyen fájlok vannak stb.

Nagyon jól jön, ha a munkafázisoknak és featureöknek kódja van.

