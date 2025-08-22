# A feladat

Prototípus arra, hogy a BME Smartdoc rendszerébe hogyan lehet egy Excel tábla alapján adatokat beírni, majd a kitöltött dokumentumot PDF-ként letölteni.

Mivel jobb, ha nem kell semmit telepíteni hozzá, első körben az Excel makró csak kirakja a SmartDoc számára előkészített CSV tartalmat a vágólapra, hogy a weboldalon már csak be kelljen illeszteni és letölteni a PDF-et.

Utána lehet egy másik eszközt készíteni, ami CSV fájlokból egyesével SmartDoc PDF fájlokat készít.

# Tanulságok



# Konkrét promptok

Have a look at the file #file:spec.md ! The task to implement needs interaction with a webpage (probably using javascript), and copy-pasting of the content of a file into the webpage. Beside the Excel VBA macro which is used to coordinate this procedure, what languages, environments and tools should I use for the implementation? An important goal is that I do not need to install special runtime environments on the computer to use it.

---

Have a look at #file:spec.md , do you need any further information to generate the VBA macro for feature XLS2CSV and the Python application for feature CSV2PDF?

---
(Kérdéseket tett fel, teljesen jogosan.)

The VBA macro should export all rows at once. The webpage does not need authentication, howevery it may not be available in which case a nice error message should be shown. And yes, the script should wait for the download. Please update #spec.md according to these.

---