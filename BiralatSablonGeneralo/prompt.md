# A feladat

A spec.md specifikáció alapján Excel és Word VBA makrók generálása bírálati sablon készítésre, majd nyomtatható PDF generálására. A hallgató adatai a tanszéki portál konzulens exportjából kitöltődnek.

# Tanulságok

- A specifikációt nagyon megéri hivatkozható kódnevekkel ellátni, és ennek ténye benne lehet a specifikáció elejében. Az AI is szépen használja a kódneveket.
- Hatékonyan lehet vele VBA makrókat készíttetni, bár néha nem létező metódusokat hív, amire fel kell hívni a figyelmét és akkor javítja. (Excel és Work eltérései miatt például.)
- Nagyon belegabalyodott a páratlan oldal hosszú bírálat esetén beszúrandó üres oldalba és nagyon nem haladtunk előre vele...

# Konkrét promptok

Have a look at the file @spec.md and create VBA Excel macro for the feature (INITLIST).

---

Now create the VBA macro for the feature (GENDOCX) into the file GenDocx.bas

---

Now create the Word VBA macro for feature (GENPDF).

---

Member not found error in "Application.CutCopyMode = False"

---

If the review part is 1 page long, you add 2 additional pages instead of only 1.

---

We also need padding for 1-page review because we are duplicating it inside the document and the two instances should be printed on separate paper sheets.

---
