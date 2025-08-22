# A feladat

Prototípus arra, hogy a BME Smartdoc rendszerébe hogyan lehet egy Excel tábla alapján adatokat beírni, majd a kitöltött dokumentumot PDF-ként letölteni.

Mivel jobb, ha nem kell semmit telepíteni hozzá, első körben az Excel makró csak kirakja a SmartDoc számára előkészített CSV tartalmat a vágólapra, hogy a weboldalon már csak be kelljen illeszteni és letölteni a PDF-et.

Utána lehet egy másik eszközt készíteni, ami CSV fájlokból egyesével SmartDoc PDF fájlokat készít.

# Tanulságok

Amikor szóltam, hogy az Excel makró nem UTF-8-ba exportál, azt kijavította, de utána a régi export fájlokkal tesztelte a következő (Python) featuret és mivel a régi fájlok még más kódolással készültek, egyből módosította a Python kódot is, hogy a legacy fájlokat is támogassa.

Készített a VBA scritbe egy teszt sub-ot és mondta, hogy most tesztelni fogja, pedig nem is tudja futtatni. (Kézzel kitöröltem.)

Csomószor elrontotta, hogy virtual env python futtatás kell, meg hogy melyik könyvtárból kell indítania. Készíttettem vele erre egy batch filet és most már azt használja szépen.

CSV fájl tartalom copy-paste webre: az UTF-8 BOM-ot (Byte Order Mark) is odamásolta, amitől a weboldal megbolondult. Kimásoltam neki egy fájlba, hogy ő mit copy-pastelt be és ebből rájött, mi a gond.

# Konkrét promptok

Have a look at the file #file:spec.md ! The task to implement needs interaction with a webpage (probably using javascript), and copy-pasting of the content of a file into the webpage. Beside the Excel VBA macro which is used to coordinate this procedure, what languages, environments and tools should I use for the implementation? An important goal is that I do not need to install special runtime environments on the computer to use it.

---

Have a look at #file:spec.md , do you need any further information to generate the VBA macro for feature XLS2CSV and the Python application for feature CSV2PDF?

---
(Kérdéseket tett fel, teljesen jogosan.)

The VBA macro should export all rows at once. The webpage does not need authentication, howevery it may not be available in which case a nice error message should be shown. And yes, the script should wait for the download. Please update #spec.md according to these.

---

Update the macro to use semicolon as separator in the CSV file and use quotation marks to surround every value in it.

---

When getting the index of the last row, do not assume that every cell in every row is filled in. Only use the "filename column" for this as that column surely contains a value for every data row.

---

Now the macro asks for the filename column twice. Keep only the first one.

---

Now the xls2csv feature is ready. Proceed to csv2pdf and implement it.

---

The Excel macro in xls2csv.bas exports CSV in some other encoding and not UTF-8. Please fix it to use UTF-8 everywhere.

---

Now I have removed all legacy CSV files and we will not meet them anymore. Remove the legacy encoding support from the Python application. You can assume that every input CSV is now consistently UTF-8 encoded.

---

The SmartDoc system told me: "A dátumot n, nn, hnn, hhnn, éhhnn, ééhhnn, ééééhhnn, éééé-hh-nn, éééé.hh.nn vagy éééé. hh. nn formátumban lehet megadni." According to this, modify the VBA macro to export all dates in the format YYYYMMDD.

---

Now lets test the csv2pdf feature. Please start your python script to process all CSV files in the root directory of the project.

---

Modify the python script to wait 5 seconds after every web browser operation. Put this 5 second into a constant in the beginning of the file so it is easy to modify.

---

Temporarily comment out the "CSV => HTML" button click in the python script. Instead of that, wait for the user to perform this click in the browser manually. Then, resume the process.

(Nem mondtam neki, hogy a konzolban várjon jelzésre...)

---

You keep on failing to start the script because you are in the wrong directory, fail to change it, or forget to start the virtual environment. Create a batch file in the root directory to automate these steps.

---

There is an issue with the copy-pasting of the CSV content into the textfield on the website. I copied the content what you pasted in into the file #file:delme.txt . You copy-pasted the content of #file:Minta Béka.csv . In the beginning of your pasting, there is some special character which is not in there in the original CSV file. Fix the python script not to send that special character.

(Szerintem BOM hiba, javította.)

---

Make the README.md up-to-date w.r.t. how to start the two features of the project after each other. Mention the batch file you created to start the python script.

