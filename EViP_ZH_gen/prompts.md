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

TODO: group tests according to subtasks

(Note: VS -> VSCode átálláskor *.md encoding hiba, ha úgy marad, később megpróbálja a rosszat követni. Érdemes rögtön minden fájlt javíttatni vele.)

