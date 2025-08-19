# A feladat

Régi Info2 kérdésbankből igaz-hamis kérdések exportálása Gift formátumba, abból JSON készítése mintamegoldással és csak kérdésekkel. ChatGPT5 webes felületen megválaszolta őket (86%), majd VS Code alatt (Claude Sonnet 4 Agent) kiértékelés és magyarázatok hozzáadása.

Kiegészítésként félreérthető kérdések keresése, valamint az igaz-hamis kérdések ABCD kérdésekké alakítása generált hamis válaszokkal és az eredeti kérdés átfogalmazásával.

# Tanulságok

- **Formátum átalakításra jobb scriptet kérni**: a gift->json átalakítás elég időigényes volt, de sikerült. (Ellenőrizni kell, hogy minden kérdés átment-e, mert egy GPT modell csak 15-öt rakott át a 109-ből.)
- A helyes válaszok null-ra cserélésére az agent **magától** vetette fel, hogy **scriptet ír rá és futtatja**, mert az hatékonyabb.
- **A sima összehasonlítós kiértékelést is át kell nézni!** A kiértékelésnél bekerült egy "ez hamis és ez így is van, de az indoklás fontos..." eredmény, amit fura módon ezért hibásnak számolt. Kérésre javította, de elsőre hibás lett a kiértékelés, pedig csak az igaz-hamis válaszokat kellett összevetnie a helyes megoldással!
- Hatékonyan **keresett félreérthető kérdéseket**, bár volt, amit félreértett.
- Nagyon szépen készített az **eredeti kérdésekből ABCD (multiple choice) kérdéseket** hibás válaszokkal együtt. Csak ki kellett emelni, hogy fogalmazza át a kérdéseket, hogy már ne igaz-hamis kérdések legyenek, mert akkor a válaszok között 3 igaz és 1 hamis vagy fordítva volt, ami elég triviális.

# Konkrét promptok

The file #file:export.gift is in Gift format used by Moodle for exporting tests. Please create a "questions_with_correct_answers.json" file containing all the questions with the question texts and the correct answer.

**Tanulság: ez nagyon sokáig tart neki.**

Now create a copy of the #file:questions_with_correct_answers.json  file called exam.json with the "answer" fields all set to NULL.

**Zseniális, gyorsan parancssorba készítette el a transformációt!**

## A ChatGPT webes felületén feltöltve a kérdéseket:

You are a very clever student. I will give you a list of true/false questions in JSON format. Please modify the file and include the correct answer into the "answer" field of the JSON format as "true" or "false". Replace the current "null" value there. The questions are in hungarian.

**Elsőre megszakadt a feldolgozás, mert túl hosszú a lista. Darabokban dolgozza fel. 40-essével dolgozta fel és a háttérben összefűzte, nekem csak 40-essével azt kellett mondani, hogy igen, folytassa.**

## Megint a Visual Studio Code-ban (GPT-4.1)

Now a student has answered the questions, the result is in the file #file:exam_filled_by_chatGPT5.json  . Compare that with #file:questions_with_correct_answers.json and evaluate the answers. Create an evaluation.md file with two sections: correctly answered and questions with false responses. For the false responses, give educative feedback to the student in hungarian. At the beginning of the file, put an evaluation as percentage of correct answers.

**Na ezen azért egy ideig kellett dolgoznia...**

## Egy nagyon érdekes válasz a kiértékelésben:

### 10. TCP protokoll esetén ha egy csomag nem érkezik meg, de az utána következők igen, akkor az elveszett csomag utáni sikeresen átküldött csomagokat már nem kell újra elküldeni.
**A te válaszod:** hamis  
**Helyes válasz:** hamis  
**Visszajelzés:** A válaszod helyesen hamis, de a magyarázat fontos: TCP esetén ha egy csomag elvész, de az utána következők megérkeznek, akkor a hiányzó csomagot újra kell küldeni, de a már sikeresen megérkezett csomagokat nem.

**És ezt ezért hamisnak tekintette!!!**

## Félreérthető kérdések keresése

Have a look at #file:questions_with_correct_answers.json . Are there questions which you consider confusing for the students? Which ones need improvement?

**Volt, amit félreértett, de voltak jó tippek is benne.**

## Az első pár kérdésből multiple choice kérdés gyártása, hibás válaszok generálásával

Now take first 5 questions from #file:questions_with_correct_answers.json . Turn every question into a multiple-choice question with 1 correct and 3 wrong answers. Put these new multiple-choice questions into a new file called mcq-1.md

**Az igaz/hamis kérdéseket megtartva minden válaszban volt 1 igaz és 3 hamis vagy fordítva, ami miatt könnyű tippelni.**

By looking at the answers for your questions there are always either 3 false and 1 true, or 3 true and 1 false answers which makes it very easy to guess.
Rephrase the questions and put them into the new file mcq-2.md where the questions are not true/false questions anymore. Preserve the focus of the questions but rephrase them to be non-true/false questions. So that the 4 possible answers can have more diversity than true and false with some reasoning.

**Nagyon király! Tényleg átalakította ABCD kérdésekké és egész jó hamis válaszokat is generált hozzá!**
