# These are the prompts I used to generate the specification for the topic retrieval application using AIStudio

Hello! I need your help to create the specification for a console application which retrieves data from a website and stores them in JSON format. The data is about education courses where students can choose topics. Every topic has an advisor, a student count limit, title and description, and it is assigned to a set of courses. Only students on those courses can choose the topic. Students enroll themselves into various courses before choosing a topic. These courses belong to some categories based on education level (BSc or MSc) and curriculum (IT engineer (in hungarian Mérnök Informatikus), electrical engineer (Villamosmérnök), mechatronic engineer (Mechatronikai mérnök)).

There are separate web pages listing the topics for the categories above. I want the application to check these pages and collect the data from the topics appearing there. Every topic has a separate page with its details. I want the application to visit all these pages and retreieve its URL, list of names of advisors (in hungarian "konzulens"), and the student count limit. And whether it is an external topic offered by a company or an internal one offered by our department.

The pages corresponding to the topic categories are the following:

- BSc level
    - IT engineering
        - Project laboratory: https://www.aut.bme.hu/Education/BScInfo/Onlab
        - Thesis project: https://www.aut.bme.hu/Education/BScInfo/Szakdolgozat
    - Electrical engineering
        - Project laboratory: https://www.aut.bme.hu/Education/BScVillany/Onlab
        - Thesis project: https://www.aut.bme.hu/Education/BScVillany/Szakdolgozat
    - Mechatronic engineer:
        - Thesis project: https://www.aut.bme.hu/Education/BScMechatronika/Szakdolgozat
- MSc level
    - IT engineering
        - Project laboratory: https://www.aut.bme.hu/Education/MScInfo/Onlab
        - Thesis project: https://www.aut.bme.hu/Education/MScInfo/Diploma
    - Electrical engineering
        - Project laboratory: https://www.aut.bme.hu/Education/MScVillany/Onlab
        - Thesis project: https://www.aut.bme.hu/Education/MScVillany/Diploma
    - Mechatronic engineer:
        - Project task: https://www.aut.bme.hu/Education/MScMechatronika/Onlab
        - Thesis project: https://www.aut.bme.hu/Education/MScMechatronika/Diploma

On the pages of these categories, you can find the list of related courses under "Kapcsolódó tárgyak". The most important is the course code which always starts with "VIAU". (The official code should have a university level "BME" prefix as well, so you should add that when storing it, make is start with "BMEVIAU".)

The topics are listed under "Kiírt témák". Each of them is a link to its details page. The text of the link is the title of the topic.

## The details page of a topic

In the detail page, for example in https://www.aut.bme.hu/Task/25-26-osz/LLMalapu-informaciokereso you can find the most important information as follows:

- Save whether this is an external topic. External topics have an external partner mentioned as "Külső partner:" followed by the company name. On the example page above it is "Zenitech".
- Student count limit is written after "Maximális létszám:", in the example above, it is 2: "2 fő".
- List of supervisors is listed under "Konzulensek" in a separate area on the right side of the page.
- List of courses where students can choose this topic. The available course groups are listed under "Válassza ki a képzést és tárgycsoportot" in a dropdown list, and for every choice, the dropdown list below that (under "Válassza ki a neptunban felvett tárgyat. Ügyeljen a neptun kódra!") contains the individual courses with their course code in brackets like "VIAUAL01".

## Check the descriptions above and improve it

Now first I want you to have a look at the web pages mentioned above and check wheter you will be able to generate a specification which is enough to generate an application for the task.

Does it help if I show you the web pages mentioned above with screen sharing? You can ask your questions there as well.

(AI cannot find dropdown list of courses, needs clarification.)

---

In the topic details page https://www.aut.bme.hu/Task/25-26-osz/LLMalapu-informaciokereso the two dropdown lists (selectors in HTML) have id="ddlCourseGroup" and id="ddlCourse". The options of these selectors are what you need. Can you find them now?

-----

If that information is loaded dynamically, can you still use a simple HTTP client in the python code or do you need selenium for it?

----

OK. Now please create the detailed specification for me.

----
