# A feladat

Előadás PPT-k alapján ZH feladatsor generálása: először specifikációk (többféle feladat felvetés), majd az egyikből részletes és alfeladatokra bontott specifikáció, majd mintamegoldás, unit tesztek készítése. A feladatsor hivatkozik a kapcsolódó unit tesztekre.

Később mutation testing (Stryker.NET) alapján forráskód javítása, további tesztek készítése.

# Tanulságok

- A **feladat kitalálásában** is simán tud segíteni a tananyag ismeretében.
- Érdemes előre tisztázni, hogy mi **lesz magyarul** és mi angolul. Pl. forráskód kommentárjai? Főleg, ha utána az marad bent feladatként egy kiadott keretben?
- A **Stryker.NET**-et is **ő rakta fel**, csak megmutattam neki a holnapját. (Magától tudta, hogy a Getting started oldal kell neki.)
- A kezdéskor új sln-t hozott létre (Visual Studio alatt), én meg csak néztem az eredetit, amiben semmi nem változott...)
- VS alatt a chat ablak sokszor beragadt, VS Code alát átköltöztem a projekt felénél.
- **Encoding hibák VS -> VSCode átálláskor és javíttatásuk**: Ha úgy marad, később megpróbálja a rosszat követni. Érdemes rögtön minden fájlt javíttatni vele. "The file #file:prompts.md seems to have encoding issues. Please fix the hungarian characters."
- **Kérj további unit teszteket, a kódon is javít!** Ha további unit teszteket kérek, az alapján többször addigi hibákra is rájött és azokat is javította. "Now extend the test project to contain a very detailed set of tests, checking even lots of edge cases."
- **Inkább betippelte: konzol bemenet, javascriptes riport**
    - Konzol bemenet szimulálása: Interaktív konzol alkalmazás minden menüpontjára kimenet, majd markdown generálás: végül nem végignyomkodta (stdin bemenetre fájllal próbálkozott, de a Console.ReadKey() miatt nem ment neki és végül inkább szimulálta a programot.)
    - A javascriptes interaktív riport parsolása nem ment neki, helyette betippelgetett javítási lehetőségeket (És erről csak akkor szólt, amikor rákérdeztem!). Aztán megmutattam neki azt az oldalt, ahol a riporterekről ír a doksi, utána már szépen dolgozott a JSON alapján.
- **Megjelölt feladat kódját kommentárra cserélve**: Másik kiísérletből már teszteltem, hogy kommentárban megjelöl kódrészeket le tud cserélni részletes instrukciókra.
- prompts.md mellé **pitfalls.md kérése** nagyon tanulságos!

# Konkrét promptok

Have a look at #specification.md. Your first task is to create a specific exam task consisting of at least 5 main subtasks. Extend the #specification.md accordingly. Write everything in hungarian and translate the original content of the specification into hungarian as well.

---

Modify #specification.md at every subtask to include instructions on where (for example in which project) the subtask should be implemented. The tasks should be clear and concise, with a focus on practical implementation.

---

By the time of the exam, students are not expected to know about dependency injection, so do not include it in the tasks. Also remove complex date manipulation tasks. Instead of those, you can assign tasks related to regular expressions.
Please update the #specification.md accordingly.

---

The students should be able to create simple regular expressions so do not tell them in the tasks what exactly the regex pattern should be. Instead, you can provide a hint or example of what they should look for in the log entries.
Please update the #specification.md accordingly.

---

Now start the implementation, but work only on the 1st task "Projekt struktúra létrehozása".

(Tanulság: Új sln-t hozott létre, én meg csak néztem az eredetit, amiben semmi nem változott...)

---

Now create the sample solution for the 2nd subtask: "2. Naplóbejegyzés modell és szolgáltatás létrehozása"

---

Now proceed with the subtask "3. Naplófájl beolvasása és formátum validálása".

---
(FONTOS)

During your work there were some errors and pitfalls. Please create a pitfalls.md in the root directory where you summarize these, so we know what to avoid next time.

---
(FONTOS)

The file #file:prompts.md seems to have encoding issues. Please fix the hungarian characters.

---
Tanulság: na ez csak úgy ment neki, hogy legenerálta a kimenetet, de nem a programból nyerte ki. Szerinte a Console.ReadKey() nem látja a fájlból jövő standard inputot.

"Please start the console application, redirect its output to a file named "output_demo.log" and trigger all functions of the application, so that the output_demo.log file contains everything the application can show about the #file:sample.log file."

---

Turn #output_demo.log into a formatted markdown file named example_run.md

---

Now extend the test project to contain a very detailed set of tests, checking even lots of edge cases.

(Közben a kódon is tovább javított! :) )

---

Now please update #specification.md according to the new version of the test set. Keep it divided into subtasks so that students can work on them incrementally during the exam.

---

All unit tests are now in a single file #file:UnitTest1.cs . Avoid using default filenames like "UnitTest1.cs", "Form1.cs" etc. And please divide the unit tests according to the subtasks in #file:specification.md . Tell the students in the subtask descriptions which unit tests they have to make pass in that subtask.

---

(Tanulság: VS -> VSCode átálláskor *.md encoding hiba, ha úgy marad, később megpróbálja a rosszat követni. Érdemes rögtön minden fájlt javíttatni vele.)

Tanulság: ha a vizsgafeladat magyarul kell, akkor rögtön az elején érdemes figyelni rá, hogy mi egyen magyarul és mi angolul. Példul a forráskód metódus nevei, kommentárjai...

--- Stryker.net install and use

I want to use the package Stryker.NET. Have a look at its website https://stryker-mutator.io/docs/stryker-net/introduction/ . I want you to
(1) install the package for this project,
(2) launch the default analysis,
(3) analyse the results and suggest changes to improve the unit test coverage according to the report,
(4) apply the suggested changes to the codebase, and
(5) re-run the stryker.net analysis to see the achieved improvement.

Now start with step 1.

(Tanulság: 1-2 lépéseket végrehajtotta, közben talált elszálló unit teszteket, ezeket több iterációban javította.)

---

Now have a look at the Stryker.NET analysis results and suggest improvements to the codebase to reduce the number of surviving mutations.

---

There have been some errors and pitfalls with the introduction of Stryker.NET. Please extend pitfalls.md to reflect the new experiences and prepare us to be able to avoid these pitfalls later.

---
(FONTOS)

#file:LogAnalyzerService.cs has a IsPartOfVersionNumber method. Remove all tests which assume there is some kind of version number in the test log file which has to be separated from the IP addresses. No need to distinguish IP addresses and version numbers. Update the tests and the test input data accordingly.

---

Now have a look at latest the mutation testing results and create a suggestion how to significantly improve the mutation score. For example logic operation and exception throwing seems to be a common issue to address.

---

(TANULSÁG) 

Question: when you are reading the mutation testing reports, do you see the markings indicating the surviving mutations? Or are you just guessing based on the source code?

---

Have a look at the webpage https://stryker-mutator.io/docs/stryker-net/reporters/ . It contains information about how you can extract the reports of stryker.net in formats easier for you to process. Use one of those options instead.

-----

Now please update the #file:specification.md , and the #file:pitfalls.md files according to the improvements. Do not forget to remove the version vs IP address separation from #file:specification.md .
