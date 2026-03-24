# Section 1: Task description

There are a lots of small projects about AI generated scripts, macros and other tools as subdirectories. The goal is to use these to build an example based teaching material for IT engineering students. Most subdirectories contain a spec.md file as the projects specification, and a prompts.md as a summary of the dialogs with the AI. Sometimes this file is called tanulsagok.md, but you may use any other markdown files.

Your tasks are the following:

Task 1: Create Section 2 of this document where you summarize the experiences and conclusions of these small projects. 

Task 2: Create a teaching material in the form of a list of slides which cover the contents of Section 2. Put these into Section 3 and follow the format of the example there. You will need to create a title, a compact text content for the audience to read, a prompt for creating a suitable illustration picture for the slide, and you should add detailed comments for the presenter which only they will read before the presentation.

Further details:
- The target audience is hungarian, so create the summaries and slides in hungarian.
- They are IT engineering students with software development skills. They already used ChatGPT for some simple tasks but they need to improve their prompting skills. This is the current goal.
- Use all subprojects in this directory to create the teaching material.
- Focus on all aspects after each other like: Technical lessons (what works/doesn't work with AI), Process/workflow insights, Best practices for prompting, Common pitfalls and how to avoid them. These can be all a nice group of slides.

# Section 2: Summary of the projects, conclusions and experiences

## Áttekintés

A projektgyűjteményben számos kisebb AI-generált eszköz található: Excel és Word VBA makrók, Python scriptek web scraping-gel és adatfeldolgozással, C# .NET konzol alkalmazások unit tesztekkel, GitHub Pages oldal, valamint Outlook bővítmények. Ezek elkészítése során értékes tapasztalatok gyűltek össze az AI-asszisztált szoftverfejlesztés területén.

A projektek fő területei:
- **VBA makrók**: Excel és Word automatizálás (bírálati sablonok, adatgyűjtés, dokumentumgenerálás)
- **Python alkalmazások**: PDF adatkinyerés, web scraping Seleniummal, adatvizualizáció, CSV feldolgozás
- **C# .NET projektek**: LogAnalyzer unit tesztekkel és mutation testing-gel (Stryker.NET)
- **Web projektek**: Jekyll alapú GitHub Pages oldal, SmartDoc integráció
- **Adatfeldolgozás**: hőmérsékleti adatok vizualizációja, számlák feldolgozása, Neptun adatok begyűjtése

## 1. Technikai tanulságok: Mi működik jól és mi nem az AI-val?

### 1.1 Jól működő területek

**Strukturált feladatok implementálása**
- Az AI kiválóan kezeli a szintaktikai és algoritmikus feladatokat (pl. pandas csoportosítás, Excel írás, reguláris kifejezések)
- VBA, Python, C# kódgenerálás nagy hatékonysággal működik, ha a feladat egyértelmű
- Unit tesztek generálása és unit tesztek alapján a forráskód javítása kiemelkedően jó

**Refaktorálás és kódminőség javítás**
- Az AI képes SOLID elvek alapján refaktorálni
- Kódismétlések felismerése és javítása
- Ha további unit teszteket kérünk, az alapján a meglévő kódon is javít

**Hiba javítás és debuggolás**
- Konkrét hibaüzenetek alapján gyors javítások
- Encoding hibák felismerése és javítása
- Ha van egy hiba, meg lehet kérni, hogy keressen további hasonló hibákat is

**Formátum átalakítások**
- JSON, CSV, XML, GIFT formátumok közötti konverzió
- Markdown generálás program kimenetekből
- Unicode és encoding problémák kezelése

### 1.2 Gyengén működő vagy problémás területek

**Teljesítmény és optimalizálás**
- Első implementációk gyakran nagyon hatékonytalanok (pl. O(n²) helyett O(m) algoritmus kérése után)
- Excel VBA-ban minden karakterre külön háttérszín vizsgálat helyett Find.Execute használata explicit kérés után
- Outlook API használatánál minden emailre minden email végignézése

**Tényfeltárás és domain tudás**
- Személyi azonosító vs. okmányszám összekeverése
- Elavult információk használata
- Hallucinált matematikai ellenőrző összegek algoritmusai
- Csak akkor hatékony, ha a fejlesztőnek van validáláshoz szükséges tudása

**Kontextus értelmezés**
- PDF-ből adatkinyerés alapos tesztelést igényel (tizedesvessző, pont, szóköz problémák)
- Selenium használatánál nem triviális felismerni, ha login szükséges
- Hallucináció: funkcionalitások feltételezése, amik nincsenek implementálva (pl. "real-time statistics updates", "dropdown menus to assign students")

**Sablon felismerés túlzásai**
- "500042XXXX" fájlnévben az AI sablonra gondolt, pedig az X-ek konkrétan kellenek
- Fokozatos, többszöri pontosítás szükséges

## 2. Folyamat és workflow tanulságok

### 2.1 Specifikáció menedzsment

**Strukturált specifikáció előnyei**
- Érdemes a spec.md-t hivatkozható feature kódokkal ellátni (pl. "(DLXLS)", "(MKXLSX)", "(IN001)")
- Az AI szépen használja ezeket a hivatkozásokat később
- Feature kódok bevezetése a specifikáció elején:
  ```
  "In this section, I will assign an identifier for every function so that 
  we can easier talk about them. The identifier will be before the title 
  of the function, in brackets and may contain letters and numbers."
  ```

**Specifikáció tisztázása**
- Érdemes előre tisztázni, mi lesz magyarul és mi angolul (forráskód kommentárjai, metódus nevei stb.)
- A specifikációt át lehet nézetni az AI-val és kérdéseket tehet fel hozzá
- Details szakaszban az AI kérdéseire adott válaszok beépülnek a specifikációba

**InformationForAI.md használata**
- Hozzon létre magának jegyzetet a projektről
- Új chat indításakor gyorsabb a kontextus felépítés
- Project struktúra, fő döntések dokumentálása

### 2.2 Iteratív fejlesztés

**Fokozatos felépítés (Least-to-Most)**
- Komplex feladatoknál a zero-shot promptolás ritkán működik
- Feature-ök egyenkénti implementálása és tesztelése
- Feladat feldarabolása: például fejléc parse-olása külön, dátum hozzáadása külön, rendezés külön lépésben

**Munkafázis kérések bevezetése**
- **"Q:"** prefix: csak kérdés, ne módosítson semmit
- **"DOC:"** prefix: csak dokumentáció frissítés
- **"TEST:"** prefix: unit tesztek futtatása és javítása
- **"REFACTOR:"** prefix: refaktorálás végrehajtása

**Tesztelés és validáció**
- Folyamatos emberi validáció (human-in-the-loop) elengedhetetlen
- Unit tesztek bővítése közben edge case-ek találása
- Mutation testing (Stryker.NET) használata a tesztlefedettség javításához

### 2.3 Eszközök és környezet

**Környezet menedzsment problémák**
- Az AI elfelejti a working directory-t vagy a virtual environment aktiválását
- Megoldás: batch/shell script készítése az automatizáláshoz
- Példa: `start_app.bat` ami aktiválja a venv-et és a megfelelő könyvtárból indít

**VS Code vs Visual Studio**
- VS Code chat ablak stabilabb volt nagy projekteknél
- Encoding problémák VS → VS Code váltáskor: minden fájlt javí tartani érdemes egyszerre
- Prompt: "The file #file:prompts.md seems to have encoding issues. Please fix the hungarian characters."

**Terminal parancsok**
- PowerShell vs Bash különbségek (`;` vs `&&`)
- Az AI néha bash szintaxist használ PowerShell-ben
- Selenium: console input szimuláció Console.ReadKey() miatt nem működött file redirect-tel

## 3. Best practice-ek a promptoláshoz

### 3.1 Specifikáció alapú megközelítés

**Kétféle indítási stratégia**
1. **spec.md-vel indítás**: teljes specifikáció előre
2. **Kérdések alapján indítás**: rövid leírás, AI kérdez, válaszok után indul a munka

Mindkettő működik, de a második interaktívabb és pontosabb specifikációhoz vezet.

**Specifikáció bővítése menet közben**
- Az AI figyeli a workspace változásait
- "I have extended #spec.md" után új követelmények implementálása
- Git status alapján változások felismerése

### 3.2 Szerepkörök és megszorítások

**Persona Pattern használata**
- "Role: Senior Python engineer" → profibb, modulárisabb kód
- Típusosság, Google-stílusú dokumentáció automatikusan
- Senior szerepkör esetén dekomponáltabb kód struktúra

**Megszorítások explicit megadása**
- "no AI usage" → külső API-k nélkül dolgozik
- "no installation required" → batch/VBA/egyszerű Python megoldás
- "dependency injection is not expected from students" → egyszerűbb architektúra

### 3.3 Few-Shot és példa alapú promptolás

**Konkrét számértékek használata**
- Sablon formázásnál: "38.1 expectednél legyen vízszintes vonal, 0.25-tel felfelé 38.35, lefelé 37.85"
- Numerikus példa kényszeríti ki a helyes értelmezést
- Elvont leírás helyett konkrétan: "Így nézzen ki egy sor: TermékA | Gép1 | X"

**Példafájlok megadása**
- CSV, PDF fájl tartalmának megmutatása
- Expected output példa megadása
- Példaalapú promptolás hatékonyabb, mint szabályok leírása

**Pszeudokód magyarázat**
- Ha az AI egyszerűsíteni próbál, pszeudokóddal lehet megakadályozni
- Modulo művelet, váltakozó feldolgozás részletes leírása
- Minden részlet világosan a promptban

### 3.4 Acceptance Criteria (AC) használata

**Strukturált elvárások**
- "AC1: Parses CSV files with semicolon separator"
- "AC2: Detects irregular patches"
- "AC6: Completes on a workbook with a sheet of 100k rows"
- Pontosan definiált siker kritériumok

**Hibakezelési követelmények**
- Log errors and mark as NOT_FOUND
- Mark uncertain extractions for human review
- Nice error messages, stop on error

### 3.5 Explicit utasítások a hibák elkerülésére

**Túlzott egyszerűsítés megakadályozása**
- "Do not assume X", "Check for Y condition"
- Például: ne feltételezze, hogy minden cella kitöltött
- Ne használjon default fájlneveket (UnitTest1.cs, Form1.cs)

**Kód organization**
- Teszt fájlok feladatokra bontása
- Moduláris felépítés kérése
- SOLID elvek explicit említése

## 4. Gyakori buktatók és elkerülésük

### 4.1 Performance buktatók

**Probléma: Hatékony algoritmus hiánya**
- Első megoldás: minden karakterre egyesével vizsgál (O(n))
- Megoldás: "Can you use a solution which runs faster? For example by searching for yellow highlights in advance?"
- Eredmény: Find.Execute használat, O(m) ahol m << n

**Probléma: Outlook API lassúsága**
- Minden emailre minden email végignézése
- Regex illesztések pontos match helyett végződés ellenőrzés
- Megoldás: szűrési feltételek pontos megfogalmazása

### 4.2 VBA specifikus buktatók

**Probléma: Makró kinyírja önmagát**
- VBA makró megnyitja a saját fájlját és bezárja
- Megoldás: "The macro should not open the file again which it is running in"

**Probléma: Nem létező metódusok**
- Excel és Word VBA különbségei miatt nem létező metódusok hívása
- Megoldás: pontos platform megjelölés, hibaüzenetek alapján javítás

**Probléma: Excel formula nyelvezet**
- VBA kódba angol függvénynevek kellenek, még magyar Excel-ben is
- Példa: `VLOOKUP` nem `FKERES`

### 4.3 Fájlkezelési és encoding problémák

**Probléma: UTF-8 BOM karakterek**
- VBA makró Copy-paste-nél BOM karakter is bekerül
- Web oldal megblokkul tőle
- Megoldás: kimásoljuk egy fájlba, megmutatjuk neki, rájön

**Probléma: Encoding inkonzisztencia**
- Excel makró nem UTF-8-ba exportál
- Python script legacy encoding support-tal reagál
- Megoldás: korai megbeszélés az encoding-ról, következetes használat

**Probléma: CSV separator és quotation**
- Tizedesvessző vs pont vs szóköz pénzösszegekben
- Megoldás: "Use semicolon as separator and quotation marks for every value"

### 4.4 Selenium és web scraping buktatók

**Probléma: Login szükségessége nem felismert**
- Publikusan más a tartalom, mint bejelentkezve
- Dropdown list nem létezik publikus nézetben
- Megoldás: "wait for the user to login" utasítás beépítése

**Probléma: Túl sok elemre klikkel**
- Témák mellett konzulensek nevei is linkek
- Megoldás: szűrési feltételek finomítása (csak `BMEVI*` kódok, "Dr. Csorba Kristóf" szöveg jelenléte)

**Probléma: Wait time-ok**
- 2 másodperc túl kevés, 5 túl sok
- Megoldás: konstans változóban, könnyen módosítható
- Neptun esetén 5 másodperc biztos, utána tesztelni lehet 2-vel

### 4.5 Tesztelési buktatók

**Probléma: Tesztadatok path resolution**
- Relatív path működik solution root-ból, de nem test project-ből
- `sample.log` vs `../../../sample.log`
- Megoldás: `Path.GetTempFileName()` használat, programozott tesztadat generálás

**Probléma: Test expectation hibák**
- Várt érték helytelen (4 vs 5 user)
- Megoldás: tesztadat count előre, manuális validálás

**Probléma: Namespace conflict**
- `namespace LogAnalyzer.Console;` → `Console.WriteLine()` nem működik
- Megoldás: ne használjunk .NET system class neveket namespace-ként

### 4.6 Kontext szűkülés és lassulás

**Probléma: Conversation history növekedése**
- Egy idő után lassulás ("summarizing conversation history...")
- Korábbi helyes megoldások figyelmen kívül hagyása
- Megoldás: új chat indítása, InformationForAI.md használata

**Probléma: Félreértés felhalmozódása**
- Encoding hiba marad, később megpróbálja követni a rossz formátumot
- Regression: korábbi helyes működés elveszik
- Megoldás: minden encoding hibát egyszerre javíttatni

### 4.7 Dokumentáció és hallucinálás

**Probléma: Nem létező funkciók dokumentálása**
- README-ben dropdown menük, real-time updates említése
- Teszt függvények generálása, melyeket nem tud futtatni
- Megoldás: dokumentáció explicit felülvizsgálata, tényleges futtatás

**Probléma: Mutation testing report értelmezés**
- Stryker.NET HTML report-ot nem látja jól
- Tippelés a forráskód alapján
- Megoldás: JSON format használata, easier-to-process formátum kérése

### 4.8 Multi-repository és tooling

**Probléma: 10 git repository kezelése**
- Fájl szétmásolása minden repóba
- Commit és push mindenhova
- Megoldás: kérni lehet az AI-tól, labor anyagok kezeléséhez praktikus

## 5. Időmegtakarítás vs. időbefektetés elemzése

### 5.1 Nagy nyereség

- Strukturált, jól definiált feladatok implementálása (kódírás gyorsasága 5-10x)
- Boilerplate kód generálása (projekt struktúra, unit tesztek vázak)
- Refaktorálás és kódminőség javítás
- Dokumentáció generálása forráskódból
- Formátum konverziók (JSON, CSV, XML, Markdown)
- Mutation testing alapú kódjavítás

### 5.2 Kis nyereség vagy semleges

- PDF parsing, adatkinyerés (sok iteráció kell)
- Komplex web scraping Seleniummal (sok edge case)
- Performance optimization (explicit kérés kell)

### 5.3 Időbefektetés vagy veszteség

- Tényfeltárás domain tudás nélkül (hallucinált ellenőrző összegek, elavult info)
- Regression-ök javítása (korábbi helyes működés elveszik)
- Félreértések kiszűrése (pl. sablon vs konkrét értékek)
- Hallucinált funkciók dokumentációból törlése

**Összegzés**: Az AI-asszisztált fejlesztés hatékonysága legnagyobb, ha mérnöki pontosságú, strukturált prompt-okat használunk, folyamatos validációt végzünk, és van domain tudásunk a feladat területén.

# Section 3: Teaching material slides

## Slide 1: this is a tempate slide

### Title

XYZ

### Content

- Some content
- Some more content
- Even more content

This subsection should be compact because it will be shown to the audience during the presentation.

### Illustration image creation prompt

As most slide should have an illustration image, add the prompt for generating a suitable image for the current slide.

### Comments for the presenter

Here are comments and background information which is meant for the presenter. Here you can explain the "Content" subsection in details.
