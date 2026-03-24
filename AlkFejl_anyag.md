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

## Slide 1: Bevezetés - AI-asszisztált szoftverfejlesztés a gyakorlatban

### Title

AI-asszisztált szoftverfejlesztés: Valós projektek tanulságai

### Content

- **20+ kisebb projekt** különböző területeken
- VBA makrók, Python scriptek, C# .NET alkalmazások
- Valós automatizálási feladatok megoldása AI segítségével
- Konkrét példák: **mit érdemes** és **mit nem érdemes** AI-val csinálni
- **Cél**: hatékonyabb prompt írás, reális elvárások

### Illustration image creation prompt

Create a professional illustration showing a developer sitting at a computer with split screen: on one side various code snippets (Python, VBA, C#) floating in the air, on the other side a friendly AI assistant icon providing suggestions. Include icons representing Excel, Word, databases, and web pages. Modern, technical style with blue and green accent colors.

### Comments for the presenter

A projektgyűjtemény több mint 20 különböző megvalósítást tartalmaz, amelyek lefedik a tipikus IT feladatokat: Excel és Word automatizálás VBA-val, Python adatfeldolgozás és web scraping, C# alkalmazásfejlesztés unit tesztekkel, web projektek. A közös pont, hogy minden projekt AI asszisztencia mellett készült (főként GitHub Copilot és ChatGPT használatával).

Fontos hangsúlyozni, hogy ezek valós feladatok voltak, nem oktatási célra kitalált példák - így a tanulságok is valósak és gyakorlatiak. A projektek során felmerülő problémák ugyanazok, amikkel a diákok is találkozni fognak.

A dia célja a kontextus beállítása: nem arról van szó, hogy az AI mindent megold, hanem arról, hogy hol és hogyan érdemes használni, és milyen technikákkal kapunk jobb eredményeket.

## Slide 2: Az AI erősségei - Strukturált feladatok

### Title

Miben jeleskedik az AI? - Strukturált implementáció

### Content

- ✅ **Szintaktikai feladatok**: pandas, Excel írás, regex
- ✅ **Kódgenerálás**: VBA, Python, C# nagy hatékonysággal
- ✅ **Unit tesztek** automatikus generálása
- ✅ **Refaktorálás**: SOLID elvek, kódismétlés felismerés
- ✅ **Debuggolás**: konkrét hibaüzenetek alapján gyors javítás
- 🎯 **Sebesség**: 5-10x gyorsabb jól definiált feladatoknál

### Illustration image creation prompt

Create an illustration showing a speedometer with the needle pointing to "10x" speed, surrounded by code elements: unit test symbols (checkmarks), refactoring arrows showing code transformation, bug icons being fixed, and various programming language logos (Python, C#, VBA). Use green colors to indicate success and efficiency.

### Comments for the presenter

Ez a dia az AI legnagyobb erősségeit mutatja be. Fontos kiemelni, hogy "strukturált feladat" alatt olyan implementációt értünk, ahol:
1. A feladat jól definiált
2. Van egyértelmű input és output
3. A megoldási logika leírható

**Konkrét példák a projektekből:**
- **Unit tesztek**: A LogAnalyzer projektben az AI generálta a teljes test suite-ot, majd amikor edge case-eket kértünk, nemcsak új teszteket írt, hanem a production kódot is javította
- **Refaktorálás**: Több projektben is, amikor hosszúra nőtt a kód, SOLID elvek alapján szétszedte modulokra
- **Debuggolás**: Encoding hibák, namespace konfliktusok - konkrét hibaüzenet alapján azonnal javított

A 5-10x sebességnövekedés nem túlzás! Boilerplate kód, projekt struktúra felállítása, tesztvázak - ezek perc alatt megvannak, szemben a manuális órákkal.

**Figyelem**: Ez csak akkor igaz, ha a feladat strukturált! (Lásd következő diákat a gyengeségekről.)

## Slide 3: Az AI gyengeségei - Teljesítmény és optimalizálás

### Title

Miben gyenge az AI? - Performance problémák

### Content

- ❌ **Első implementációk gyakran hatékonytalanok**
  - O(n²) algoritmusok alapértelmezetten
  - Excel VBA: minden karakterre külön vizsgálat
  - Outlook API: minden emailre minden email végignézése
- 💡 **Megoldás**: explicit kérés az optimalizációra
  - "Can you use a faster solution?"
  - Konkrét példa: O(n) → O(m) ahol m << n

### Illustration image creation prompt

Create a visual showing two paths: a slow, winding complicated path with many loops (labeled "First implementation O(n²)") versus a fast, direct arrow path (labeled "Optimized O(m)"). Include a snail on the slow path and a rocket on the fast path. Use red for the slow path and green for the fast path.

### Comments for the presenter

Ez az egyik legfontosabb tanulság: **az AI alapértelmezetten nem optimalizál teljesítményre**. A működő megoldást adja, ami gyakran naiv implementáció.

**Konkrét példák:**
1. **WordYellowRemover projekt**: Első verzió minden karakterre egyesével vizsgált háttérszínt és törölt. Nagyon lassú, el is állt nagy dokumentumoknál. Kérésre: Find.Execute használat, csak sárga részeket keresi meg előre → drámai gyorsulás.

2. **OutlookConversionRateExaminer**: Minden emailre végigmegy az összes emailen kapcsolat keresésénél. Nem látja, hogy Outlook API-n keresztül ez óriási overhead.

3. **Algoritmus komplexitás**: A prompt-ban szerepelt: "Performance Optimization: Changes algorithm from O(n) where n=total characters to O(m) where m=yellow ranges (typically much smaller)" - ezt explicitté kellett tenni!

**Tanulság**: Mindig teszteljünk éles adatokon! Ha lassú, kérdezzük meg: "Can you optimize this for performance?" vagy adjunk konkrét célt: "This should process 100k rows in under 10 seconds."

## Slide 4: Az AI gyengeségei - Tényfeltárás és hallucinálás

### Title

Veszélyes terep: Tényfeltárás és domain tudás

### Content

- ❌ **Hallucináció típusok**:
  - Személyi azonosító ≠ okmányszám összekeverés
  - Elavult információk (régi API-k, szabályok)
  - **Kitalált matematikai ellenőrző összegek**
  - Nem létező funkciók dokumentálása
- ⚠️ **Csak akkor hatékony, ha validálni tudjuk**
- 💡 **Megoldás**: Domain tudás + human-in-the-loop

### Illustration image creation prompt

Create an illustration showing an AI assistant with a thought bubble containing question marks and incorrect formulas. Next to it, a developer with glasses looking skeptical, holding a "fact check" stamp. Include warning triangles and a balance scale showing "Facts" vs "Hallucination". Use yellow/orange colors for warning.

### Comments for the presenter

Ez talán a **legveszélyesebb** terület az AI használatánál. A hallucinálás úgy jelenik meg, hogy az AI magabiztosan állít valótlan dolgokat.

**Konkrét veszélyes esetek a projektekből:**

1. **PII (Personal Identifiable Information) kutatás**: Az AI összekeverte a személyi azonosító számot az igazolvány okmányszámával. A generált regex szintaktikailag helyes volt, de nem a valós formátumot fedte le.

2. **Matematikai ellenőrző összegek**: A "legveszélyesebb hiba" kategória - az AI magabiztosan állított algoritmusokat, amik nem léteznek. Ha ezt nem validáljuk, súlyos hibákhoz vezet.

3. **Hallucinált funkciók dokumentációban**: A ProjectLabAdmin projektben a README azt írta, hogy "Use dropdown menus to assign students" és "Monitor real-time statistics updates" - egyik sem létezett! Az AI tipikus funkciókat feltételezett hasonló rendszerekből.

4. **Stryker.NET report**: Az AI azt állította, hogy látja a HTML report-ban a mutációkat, pedig csak a forráskód alapján tippelt.

**Tanulság a tanulsagok.txt-ből**: "A tényfeltárást igénylő feladatoknál az AI használata gyakran inkább hátráltató tényező volt. A hallucinált adatok kiszűrése néha több időt emésztett fel, mintha manuálisan végeztem volna a kutatást."

**Üzenet**: Domain tudás nélkül ne bízzuk az AI-ra a tényfeltárást!

## Slide 5: Specifikáció menedzsment - Feature kódok hatalma

### Title

Strukturált specifikáció: Feature kódok használata

### Content

- 📋 **Feature azonosítók a spec.md-ben**:
  - Példák: `(DLXLS)`, `(MKXLSX)`, `(IN001)`
  - Az AI tisztán hivatkozik rájuk később
- 📝 **Bevezetés a specifikációban**:
  ```
  "Minden funkciónak lesz egy azonosítója
  zárójelben, pl. (FEAT001)"
  ```
- ✅ **Előnyök**: egyértelmű kommunikáció, nyomon követhető

### Illustration image creation prompt

Create a document-style illustration showing a specification document with organized sections, each having colored tags/labels like "(DLXLS)", "(MKXLSX)". Show arrows connecting these labels to code snippets and chat messages, illustrating clear references. Use a blue/purple professional color scheme.

### Comments for the presenter

Ez egy egyszerű, de **rendkívül hatékony technika**, ami több projektben is bizonyított.

**Hogyan működik:**
1. A spec.md elején leírjuk, hogy feature kódokat fogunk használni
2. Minden főbb funkciónak adunk egy zárójelek közötti azonosítót
3. Később a prompt-okban egyszerűen hivatkozhatunk rájuk: "Please implement (DLXLS)" vagy "There's a bug in (MKXLSX)"

**Példa a ProjectLabAdmin projektből:**
- `(DLXLS)` - Download Excel files from portal
- `(DLNEP)` - Download Neptun data
- `(DLFUSION)` - Fuse data from both sources
- `(MKXLSX)` - Make planner Excel file

A prompt-ok ezután így néztek ki: "Now proceed to the DLNEP feature and implement it." vagy "DLNEP seems to work fine. Please update..."

**Miért jó ez?**
- **Tömör**: nem kell minden alkalommal újra leírni mit értünk a feature alatt
- **Egyértelmű**: nincs kétértelműség, melyik részről van szó
- **Trackelhető**: könnyen látszik a fejlődés
- **Skálázható**: sok feature esetén is átlátható marad

**Hasonló a unit teszt elnevezésekhez vagy a user story ID-khoz az agile fejlesztésben.**

## Slide 6: Iteratív fejlesztés - Least-to-Most stratégia

### Title

Fokozatos felépítés: Ne minden egyszerre!

### Content

- 🎯 **Zero-shot ritkán működik** komplex feladatoknál
- 📦 **Feladat feldarabolás**:
  1. Fejléc parse-olás külön
  2. Dátum hozzáadás külön
  3. Rendezés külön lépésben
- 🔄 **Feature-ök egyenként**: implementáció → teszt → következő
- ⚡ **Munkafázis prefixek**: Q:, DOC:, TEST:, REFACTOR:

### Illustration image creation prompt

Create a step-by-step staircase illustration where each step represents a feature implementation phase. Show a developer climbing the stairs, with checkmarks on completed steps. Include labels like "Parse", "Process", "Test", "Refactor". At the top, a complete application. Use progressive colors from light to dark showing advancement.

### Comments for the presenter

Ez a **Least-to-Most Prompting** stratégia, ami a kutatási irodalomban is bizonyítottan hatékony összetett problémákra.

**Miért ne egyszerre:**
- Az AI elveszti a fonalat
- Nehéz debuggolni mi ment félre
- Context overflow nagy prompt-oknál

**Konkrét példa a TemperatureMonitoring projektből:**
Ahelyett, hogy "Dolgozd fel a ZIP fájlokat, parse-old a CSV-t, konvertáld az időbélyegeket, generálj vizualizációkat" egy promptban:
1. "Parse the ZIP files and list contents"
2. "Now parse one CSV and show the structure"
3. "I have C# code for the timestamp conversion, use that logic"
4. "Now import all data"
5. "Create basic visualizations"

**Munkafázis prefixek bevezetése** (TemperatureMonitoring, ProjectLabAdmin):
- **Q:** - "From now on if I start a prompt with 'Q:', only answer my question but do not take any further action like changing source code"
- **DOC:** - csak dokumentáció frissítés
- **TEST:** - unit tesztek futtatása és javítása
- **REFACTOR:** - kód átszervezés

Ez különösen akkor hasznos, amikor már működik a kód, csak dokumentációt szeretnénk frissíteni - hogy ne rontsunk el semmit véletlenül.

## Slide 7: InformationForAI.md - Jegyzetelés a jövőnek

### Title

Kontextus megőrzése: InformationForAI.md

### Content

- 📝 **Az AI írjon magának jegyzetet**:
  - Project struktúra
  - Fő architekturális döntések
  - Feature kódok magyarázata
  - Fontos konvenciók
- 🔄 **Új chat indításkor gyors kontextus**
- 💡 **Prompt**: "Create InformationForAI.md to speed up your catch-up if we start a new chat"

### Illustration image creation prompt

Create an illustration of an AI notebook or journal labeled "InformationForAI.md" with pages showing project structure diagrams, decision notes, and architecture sketches. Show a quick "reload" or "fast forward" symbol indicating rapid context loading. Use organized, neat styling with tabs and sections.

### Comments for the presenter

Ez egy **zseniális megoldás** a context limitation problémára, ami több projektben is bevállt.

**A probléma:**
- Hosszú fejlesztés során a conversation history megnő
- Az AI lassulni kezd ("summarizing conversation history...")
- Ha új chat-et indítunk, elvesznek a korábbi döntések és kontextus
- Végigolvasni a teljes kódbázist új chat-enként időpocsékolás

**A megoldás:**
Kérjük meg az AI-t, hogy készítsen egy összefoglalót **önmagának**:
```
"If we start a new chat, you have to read the codebase again. 
To make understanding the codebase faster, create a file named 
'InformationForAI.md' where you can make any kind of notes for yourself."
```

**Mit tartalmazzon:**
- Feature kódok és magyarázatuk
- Miért döntöttünk úgy, ahogy (pl. "We avoided Selenium, use static HTML parsing instead")
- Projekt struktúra, main entry points
- Fontos korlátozások ("Must not use dependency injection")
- Workflow (pl. "Run via start_app.bat which activates venv")

**Konkrét példák:**
- TemperatureMonitoring: "The agent started to implement and recognized the specification.md I was working on in parallel"
- ProjectLabAdmin: Az AI spontán javasolta: "Let me also update the InformationForAI.md file to include information about these new heatmap visualizations"

**Profi tipp**: Időnként kérjük meg az AI-t, hogy frissítse ezt automatikusan amikor új feature-t adunk hozzá.

## Slide 8: Prompt technikák - Persona Pattern

### Title

Szerepkörök hatalma: Senior Engineer vs. Kezdő

### Content

- 👤 **Persona Pattern használata**:
  - "Role: Senior Python engineer"
- 📊 **Hatás a kód minőségére**:
  - Típusosság automatikusan
  - Google-stílusú docstring-ek
  - Moduláris, dekomponált struktúra
- 🚫 **Megszorítások explicit**:
  - "no AI usage" → külső API-k nélkül
  - "no installation required"
  - "dependency injection is not expected"

### Illustration image creation prompt

Create a side-by-side comparison showing two developers: on the left, a junior developer with messy, unstructured code snippets; on the right, a senior developer with clean, well-documented code with type hints and modules. Use professional attire and confident posture for the senior. Include code quality metrics showing improvement.

### Comments for the presenter

Ez a **Persona Pattern**, egy jól dokumentált prompting technika, aminek drámai hatása lehet a generált kód minőségére.

**Miért működik:**
Az AI különböző "viselkedési mintákat" tanult meg különböző szerepkörökből. Ha senior role-t adunk, aktiváljuk azokat a mintákat, amik professzionális kódra jellemzők.

**Konkrét példa a tanulsagok.txt-ből:**
```
"A promptot a 'Role: Senior Python engineer (no AI usage)' 
utasítással indítottam. [...] Ennek hatására a modell azonnal 
alkalmazta a Python típusosságát, a Google-stílusú dokumentációs 
kommenteket és a moduláris felépítést."
```

**Mit kapunk senior role esetén:**
- Type hints automatikusan: `def process_data(items: List[Dict]) -> pd.DataFrame:`
- Docstringek Google/NumPy style-ban
- Proper error handling
- Separation of concerns
- Single Responsibility principle

**Megszorítások explicit megadása:**
Szintén fontos! Ne feltételezzük, hogy az AI tudja, mi a kontextus:
- **"no AI usage"** - ne használjon ChatGPT API-t vagy hasonlót
- **"no installation required"** - batch/VBA/pure Python megoldás
- **"students don't know dependency injection"** - egyszerűbb architektúra

**ExpertCvCollection projektnél**: "Fontos tapasztalat, hogy az AI-val generált kód karbantarthatósága jó, mivel a kikényszerített tiszta kódolási elveknek köszönhetően a forráskód olvasható és módosítható maradt."

## Slide 9: Few-Shot prompting - Konkrét példák ereje

### Title

Mutasd meg, ne magyarázd: Few-Shot technika

### Content

- 🎯 **Konkrét példák > elvont leírás**
- 🔢 **Számértékekkel**:
  - "38.1 expectednél legyen vonal, ±0.25 → 38.35 és 37.85"
  - Numerikus példa kikényszeríti a helyes értelmezést
- 📁 **File tartalom megmutatása**:
  - CSV példa sorok
  - Expected output formátum
- ✅ **Eredmény**: kevesebb félreértés, gyorsabb konvergencia

### Illustration image creation prompt

Create an illustration showing a teacher pointing at a blackboard with concrete examples (numbers, file formats, expected outputs) on the left side with happy checkmarks, versus abstract descriptions on the right side with confused question marks. Use clear contrast between the two approaches with green for examples and red for abstract.

### Comments for the presenter

Ez a **Few-Shot Prompting** - az egyik legerősebb technika az AI-val való munkánál. Az alapelv: **mutass példát ahelyett, hogy szabályokat magyaráznál**.

**Konkrét példa 1 - tanulsagok.txt:**
```
"A legfontosabb tanulság, hogy amikor részletesen, elméleti síkon 
próbáltam elmagyarázni a logikát, a modell gyakran félreértette. 
Ezzel szemben, amikor konkrét példát mutattam a kívánt kimenetre 
– például: 'Így nézzen ki egy sor: TermékA | Gép1 | X' –, 
az AI sokkal gyorsabban és pontosabban ismerte fel a mintázatot."
```

**Konkrét példa 2 - Grafikon tűréshatárok:**
```
"Amíg csak szövegesen írtam le, a modell a felső és alsó tűrést 
sokszor önálló határértékként kezelte. A fordulópont: 
'azt szeretném látni, hogy a 38.1 expectednél legyen egy vízszintes 
vonal, ehhez képest 0.25-tel felfelé és lefelé egy-egy új vonal, 
vagyis 38.35 és 37.85'"
```

A numerikus példa **kényszerítette ki**, hogy az expected köré építse a vonalakat!

**Konkrét példa 3 - BillSummarizer CSV:**
```
"examples/Fotav_szamla_pelda.pdf has a price 6267 Ft, 
issue date ('számla kelte' in hungarian) 2025.08.14., 
the provider ('Szolgáltató neve') is BKM Nonprofit Zrt."
```

Konkrét file-t megmutatva, milyen adatok vannak benne.

**Tanulság**: "A vizuális példák és a konkrét adatsorok megadása drástikusan csökkentette a félreértéseket, bizonyítva, hogy a modell gyakran jobban tanul a mintákból, mint a szabályleírásokból."

## Slide 10: Acceptance Criteria - Mérhető elvárások

### Title

Acceptance Criteria: Pontosan mit jelent a "kész"?

### Content

- ✅ **Strukturált elvárások felsorolása**:
  - AC1: Parses CSV files with semicolon separator
  - AC2: Detects irregular patches
  - AC6: Completes on 100k rows in <10 seconds
- 🎯 **Siker kritériumok pontosan definiálva**
- 🐛 **Hibakezelés specifikálása**:
  - Log errors and mark as NOT_FOUND
  - Nice error messages, stop on error

### Illustration image creation prompt

Create a checklist illustration with multiple completed checkboxes labeled "AC1", "AC2", "AC3" etc. Show measurable criteria like performance metrics, output formats, and error handling specifications. Include a "Definition of Done" badge. Use professional project management style with green checkmarks.

### Comments for the presenter

Az **Acceptance Criteria (AC)** technika közvetlenül az agile/scrum világából jön, és kiválóan működik AI prompt-oknál is.

**Miért jó ez:**
- **Egyértelmű**: nincs "kb. működjön" szintű követelmény
- **Tesztelhető**: AC alapján lehet validálni
- **Átadható**: ha új chat-et indítunk, az AC-k alapján folytathatjuk

**Konkrét példa a tanulsagok.txt-ből:**
```
"'Acceptance Criteria' (AC) pontok részletes felsorolása volt 
a promptban. Pontosan definiáltam, hogy mit tekintünk sikernek: 
például 'AC2: Detects irregular patches' vagy 
'AC6: Completes on a workbook with a sheet of 100k rows'."
```

**További AC példák a projektekből:**

**BillSummarizer:**
- AC1: Extracts amount, date, provider, address from PDFs
- AC2: Handles Hungarian text and special characters
- AC3: Outputs CSV with semicolon separator
- AC4: Date format YYYY.MM.DD
- AC5: Marks failed extractions as NOT_FOUND

**Hibakezelési AC-k:**
- "Log errors and mark as NOT_FOUND"
- "Mark uncertain extractions for human review"
- "Show nice error messages and stop on error"

**Performance AC-k:**
- "Completes on 100k rows in under 10 seconds"
- "Memory usage below 500MB"

**Összegzés a tanulsagok.txt-ből:**
"A mérnöki pontosságú, korlátokat és kritériumokat tartalmazó promptok képesek kiváltani a hosszú iterációs folyamatokat, és azonnal ipari minőségű kódot eredményeznek."

## Slide 11: Performance buktatók elkerülése

### Title

Gyakori buktató: "Működik, de lassú"

### Content

- ⚠️ **Első implementáció = naiv algoritmus**
  - WordYellowRemover: minden karakter egyenként → LASSÚ
  - Megoldás: Find.Execute, csak sárga részek
- 🔧 **Explicit kérés az optimalizációra**:
  - "Can you use a faster solution?"
  - "Search for yellow highlights in advance"
- 📊 **Eredmény**: O(n) → O(m) ahol m << n
- ✅ **Tanulság**: Mindig tesztelj éles adatmennyiségen!

### Illustration image creation prompt

Create a before/after comparison showing a slow loading bar stuck at 10% with a sad face (labeled "First implementation: check every character") versus a completed progress bar at 100% with celebration (labeled "Optimized: Find.Execute"). Include performance metrics showing the dramatic improvement.

### Comments for the presenter

Ez az **egyik leggyakoribb buktató**: a kód működik, de éles adatokon használhatatlanul lassú.

**Miért történik ez:**
Az AI alapértelmezetten a **working solution**-t adja, nem az optimálisat. A legegyszerűbb logikát implementálja, ami átmegy a feltételeken.

**Konkrét eset 1 - WordYellowRemover:**
```
Tanulság: "Nagyon lassú és el is száll az első implementáció. 
Minden karakterre egyesével vizsgál háttérszínt és töröl, ha kell."

Prompt: "This macro seems to be very slow. Can you use a solution 
which runs faster? For example by searching for yellow highlights 
in advance?"

Válasz: "Performance Optimization:
- Uses Find.Execute to locate only yellow highlighted text
- Changes algorithm from O(n) where n=total characters to O(m) 
  where m=yellow ranges (typically much smaller)"
```

**Konkrét eset 2 - OutlookConversionRateExaminer:**
```
"Nagyon hatékonytalan kód (minden emailre minden emailt végignéz, 
ami az Outlook API-n keresztül nagyon lassú)."
```

**Hogyan előzd meg:**
1. **Tesztelj éles mennyiségen**: Ne 5 soros CSV-n, hanem 100k soroson
2. **AC-ben szerepeljen performance**: "Process 100k rows in <10 sec"
3. **Explicit kérés**: "Optimize for performance"
4. **Algoritmus komplexitás említése**: "Use O(log n) solution"

**Fontos észrevétel**: Az AI tudja a fast algoritmust! Csak alapértelmezetten a simple solution-t választja. Kérésre azonnal javít.

## Slide 12: VBA specifikus buktatók

### Title

VBA csapdák: Excel ≠ Word, magyar ≠ angol

### Content

- 💀 **Makró kinyírja saját magát**:
  - Megnyitja és bezárja a saját fájlját
  - Fix: "Do not open the file it is running in"
- 📚 **Excel ≠ Word VBA**:
  - Nem létező metódusok (pl. Application.CutCopyMode)
- 🌍 **Formula nyelvezet**:
  - VBA kódban angol: `VLOOKUP` nem `FKERES`
- ✅ **Megoldás**: Pontos platform megjelölés

### Illustration image creation prompt

Create a humorous illustration showing a VBA macro character accidentally shooting itself in the foot (representing self-deletion), next to confused Excel and Word applications trying to communicate with incompatible methods. Include a formula showing "VLOOKUP" with a checkmark and "FKERES" with an X. Use warning colors.

### Comments for the presenter

A VBA projektek során speciális buktatók merültek fel, amik nem nyilvánvalóak.

**Buktató 1 - Makró öngyilkosság:**
ExcelMergerWithMacro projektben:
```
"A makró másoláshoz megnyitotta a saját fájlját is, utána pedig 
bezárja, amivel a makró egyből kinyírta magát..."

Megoldás: "The macro should not open the file again 
(for copying from) which it is running in."
```

Ez triviálisnak tűnik, de az AI nem gondol rá automatikusan!

**Buktató 2 - Excel vs Word VBA különbségek:**
BiralatSablonGeneralo_old projektben:
```
"Member not found error in 'Application.CutCopyMode = False'"
```

Az AI Excel VBA metódust használt Word VBA-ban. Az API-k hasonlóak, de nem azonosak.

**Megoldás**: A prompt-ban pontosan jelöljük meg a platformot:
- "Excel VBA macro"
- "Word VBA macro"
- Vagy: "This will run in Word, not Excel"

**Buktató 3 - Magyar Excel, angol formula:**
tanulsagok.txt:
```
"Excel formula beszúrásakor a VBA kódba az angol neveket kell 
beírni (nálam legalábbis) még akkor is, ha a felületen magyarul 
jelenik meg..."
```

A VBA kód mindig angol függvényneveket használ (`VLOOKUP`), még akkor is, ha a magyar Excelben a felhasználónak `FKERES` jelenik meg!

**Általános tanács**: VBA-nál még fontosabb a konkrét hibaüzenetek megadása az AI-nak, mert a dokumentáció kevésbé egyértelmű, mint modern nyelveknél.

## Slide 13: Encoding és fájlkezelési buktatók

### Title

Encoding pokol: UTF-8, BOM, és ami még rosszabb

### Content

- 🔤 **UTF-8 BOM probléma**:
  - VBA copy-paste BOM karakterrel → web oldal megblokkol
  - Fix: Fájlba kimásolni, megmutatni neki
- 🔄 **Encoding inkonzisztencia**:
  - Excel nem UTF-8-ba exportál → Python legacy support
  - Fix: Korai egyeztetés, következetes használat
- 📊 **CSV separator és decimálok**:
  - Tizedesvessző vs pont vs szóköz → parsing hiba
  - Fix: "Use semicolon separator, quotation marks for all values"

### Illustration image creation prompt

Create an illustration showing file encoding chaos: documents with different encoding labels (UTF-8, BOM, ISO-8859-1) causing confusion. Show a tangled mess of characters on one side, and clean, properly encoded text on the other. Include CSV format symbols and decimal separators. Use contrasting red (chaos) and green (fixed) colors.

### Comments for the presenter

Az encoding problémák **alattomos bugok** forrásai, amiket az AI nem mindig ismer fel automatikusan.

**Buktató 1 - UTF-8 BOM karakter:**
SmartdocKitolto projektben:
```
"CSV fájl tartalom copy-paste webre: az UTF-8 BOM-ot 
(Byte Order Mark) is odamásolta, amitől a weboldal megbolondult. 
Kimásoltam neki egy fájlba, hogy ő mit copy-pastelt be 
és ebből rájött, mi a gond."
```

A BOM egy láthatatlan karakter a file elején, ami jelzi az encoding-ot. A legtöbb rendszer nem szereti.

**Debugging módszer**: Ha valami látszólag jól néz ki, de nem működik → mentsd fájlba, nézd meg hex editorban vagy mutasd meg az AI-nak.

**Buktató 2 - Encoding domino effektus:**
SmartdocKitolto projektben:
```
"Amikor szóltam, hogy az Excel makró nem UTF-8-ba exportál, 
azt kijavította, DE utána a régi export fájlokkal tesztelte 
a Python feature-t és mivel a régi fájlok még más kódolással 
készültek, egyből módosította a Python kódot is, hogy a legacy 
fájlokat is támogassa."
```

Ez példa arra, amikor **az AI próbál segíteni, de rossz irányba megy**. A helyes megoldás: egyeztetni kezdetben, hogy minden UTF-8, és törölni a legacy fájlokat.

**Buktató 3 - CSV parsing problémák:**
BillSummarizer projekt:
```
"A PDF-ből adatkinyerés alapos tesztelést igényel. 
Pénzösszegben tizedesvessző, pont, szóköz bekavarnak."
```

**Megoldás**: Explicit specifikáció:
- "Use semicolon as CSV separator"
- "Put quotation marks around every value"
- "Use comma for decimal separator" vagy "Use dot for decimal"
- "Date format: YYYY.MM.DD"

## Slide 14: Selenium és web scraping buktatók

### Title

Web scraping: Login, wait time, túl sok klikk

### Content

- 🔐 **Login szükségessége rejtett**:
  - Publikus nézet ≠ bejelentkezett nézet
  - Dropdown nem létezik → crash
  - Fix: "Wait for user to login manually"
- ⏱️ **Wait time optimalizálás**:
  - 2 sec túl kevés, 5 sec túl sok
  - Fix: konstansba, tesztelés után finomítás
- 🖱️ **Túl sok elemre klikkel**:
  - Témák mellett konzulensek nevei is linkek
  - Fix: Precíz szűrési feltételek (pl. csak BMEVI* kódok)

### Illustration image creation prompt

Create an illustration showing a robot trying to interact with a website: on one side it's clicking everything including unwanted links (red X), in the middle it's waiting with a clock showing different times (2s vs 5s), and on the right it successfully logs in and accesses content (green checkmark). Include browser window frames and loading animations.

### Comments for the presenter

Selenium-based web scraping során **extra kihívások** jelentkeznek, amiket az AI nem lát előre.

**Buktató 1 - Login rejtett szükségessége:**
ProjectLabAdmin projekt:
```
"A selenium alapból nem lesz belépve a portálra és ha publikus 
oldalnak más olyankor a tartalma (nincsen téma jelentkezés 
dropdown list), akkor azt nem triviális észrevenni, hogy én 
miért látom és ő miért nem."

Later: "Ahhhh.... I see the issue! You need to login to the portal 
to see the selectors. Please modify the application to open the 
website and then wait for the user to log in before continuing."
```

**Megoldás**: Ha authentication kell, tervezd be a workflow-ba:
1. Selenium megnyit egy browsert
2. "Please wait for the user to login" - megállás
3. Console-ban enter után folytatás

**Buktató 2 - Wait time-ok:**
ProjectLabAdmin és SmartdocKitolto projektekben:
```
"Neptun needs time to load course details, waiting 2 seconds 
may not be enough. Make that 5 seconds for now."

Later: "DLNEP seems to work fine. A little bit slow. Please update 
the 'time.sleep(5)' waitings to 2 seconds."

SmartdocKitolto: "Modify the python script to wait 5 seconds after 
every web browser operation. Put this 5 second into a constant in 
the beginning of the file so it is easy to modify."
```

**Best practice**: Konstansba wait time, gyors iterálás tesztelésnél.

**Buktató 3 - Túl sok linkre klikkel:**
ProjectLabAdmin topic collector:
```
"The app seems to open the pages of advisors as well which is 
not required. Advisors appear in the details pages of the topics 
but we only need their names, so clicking on their name 
(it is also a link) is not necessary."
```

**Megoldás**: Precíz szűrési feltételek CSS selector-okhoz vagy tartalmi ellenőrzéshez.

## Slide 15: Tesztelési buktatók és namespace konfliktusok

### Title

Unit test csapdák: Path, expectation, namespace

### Content

- 📁 **Path resolution probléma**:
  - `sample.log` működik solution root-ból, de nem test project-ből
  - Fix: `Path.GetTempFileName()`, programozott tesztadat
- 🔢 **Test expectation hiba**:
  - Assert.Equal(4, count) de valójában 5 user van
  - Fix: Tesztadat count előre, manuális validálás
- 🚫 **Namespace conflict**:
  - `namespace LogAnalyzer.Console;` → `Console.WriteLine()` fail
  - Fix: Ne használj .NET system class neveket!

### Illustration image creation prompt

Create a split-screen showing three common test failures: file path errors with broken folder icons, assertion failures with "Expected: 4, Actual: 5", and namespace collision showing Console.WriteLine with a red X. Include unit test framework symbols and debugging tools. Use testing color scheme (red for failures, green for fixes).

### Comments for the presenter

A **unit teszt írás során** specifikus buktatók jelentkeztek, főleg C# .NET környezetben.

**Buktató 1 - Path resolution a tesztekben:**
EViP_ZH_gen pitfalls.md:
```
"Unit tests failed because the test couldn't find the sample log file:
string testFilePath = 'sample.log'; // File not found during test execution

Error: System.IO.FileNotFoundException: Log file not found: sample.log"
```

A working directory különböző attól függően, hogy honnan futtatjuk a tesztet (Visual Studio, dotnet test CLI, különböző könyvtárakból).

**Megoldás**:
```csharp
string testFilePath = Path.GetTempFileName();
string testContent = @"[2024-01-15 10:30:45] [ERROR] [john.doe] Test message";
File.WriteAllText(testFilePath, testContent);
try {
    var result = _service.ReadLogFile(testFilePath);
    // Assertions...
} finally {
    if (File.Exists(testFilePath)) File.Delete(testFilePath);
}
```

**Tanulság**: "Tests should be self-contained and not depend on external files"

**Buktató 2 - Test assertion értékek:**
```
Assert.Equal(4, userActivity.Count); // Expected 4, but actually had 5 users
```

Egyszerű számolási hiba, de gyakori! **Mindig manually verify** a tesztadatot.

**Buktató 3 - Namespace conflict:**
pitfalls.md:
```
namespace LogAnalyzer.Console;
class Program {
    Console.WriteLine("This fails!"); 
    // Error: 'WriteLine' does not exist in namespace 'LogAnalyzer.Console'
}
```

**Megoldás**: 
```csharp
class Program  // No namespace, or use LogAnalyzer.ConsoleApp
{
    static void Main(string[] args) {
        Console.WriteLine("This works!"); // System.Console
    }
}
```

**Lesson**: "Never use namespace names that conflict with .NET system classes"

## Slide 16: Context szűkülés és conversation management

### Title

Amikor az AI "elfárad": Context overflow

### Content

- 🐌 **Lassulás jelei**:
  - "Summarizing conversation history..."
  - Korábbi helyes megoldások elfelejteése
  - Regression-ök megjelenése
- 🆕 **Megoldás: Új chat + InformationForAI.md**
- 🔄 **Encoding domino**:
  - Egy encoding hiba marad → később követi a rossz formátumot
  - Fix: Minden encoding hibát egyszerre javíttatni
- ⚠️ **Tanulság**: Friss start, ha nem halad a munka

### Illustration image creation prompt

Create an illustration showing an AI character getting progressively tired and slow, with a growing pile of conversation messages weighing it down. Show memory/context indicators filling up. Then show a "refresh" button leading to a rejuvenated AI with a clean InformationForAI.md document. Use battery/energy metaphors.

### Comments for the presenter

Ez egy **reális probléma** hosszabb fejlesztési session-ök során, amit több projektben is tapasztaltak.

**A probléma megnyilvánulása:**

1. **Lassulás:**
TemperatureMonitoring projekt:
```
"Egy idő után kezd belassulni... és mintha ő is próbálná kezelni 
('summarizing conversation history...')."
```

2. **Regression - korábbi működés elveszik:**
SmartdocKitolto és encoding problémák:
```
"Encoding hiba marad, később megpróbálja követni a rossz formátumot"
```

3. **Félreértés felhalmozódása:**
```
"Regression: korábbi helyes működés elveszik
Megoldás: minden encoding hibát egyszerre javíttatni"
```

**Konkrét eset - SmartdocKitolto:**
```
"Amikor szóltam, hogy az Excel makró nem UTF-8-ba exportál, 
azt kijavította, de utána a régi export fájlokkal tesztelte 
a következő (Python) feature-t és mivel a régi fájlok még 
más kódolással készültek, egyből módosította a Python kódot is, 
hogy a legacy fájlokat is támogassa."
```

Az AI megpróbál "alkalmazkodni" a látott mintákhoz, de ez rossz irányba vihet!

**Megoldás stratégia:**

1. **Új chat indítása** amikor:
   - Lassulás tapasztalható
   - Regression-ök jelentkeznek
   - Érződik, hogy "nem érti már a célt"

2. **InformationForAI.md használata**:
   - Új chat gyors catch-up
   - Korábbi döntések átadása

3. **Encoding/hasonló hibák esetén**:
   - Minden affected fájlt egyszerre javíttatni
   - Prompt: "The file #file:prompts.md seems to have encoding issues. Please fix the hungarian characters."
   - Ne darabonként, mert akkor inconsistency marad

**TemperatureMonitoring projektben ez történt:**
```
"It seems we have lots of problems with the bad timestamps. 
Extend the specification to skip records with timestamp before 2020 at all."

Later: "I rolled back some changes and I start a new chat as you 
got confused and slow."
```

## Slide 17: Hallucináció az dokumentációban

### Title

Veszélyes területek: Dokumentáció hallucinálás

### Content

- 📚 **Nem létező funkciók megjelenése**:
  - "Use dropdown menus to assign students"
  - "Monitor real-time statistics updates"
  - Egyik sem létezett valójában!
- 🧪 **Teszt függvények futtatás nélkül**:
  - Készít teszt sub-ot, mondja hogy futtatja
  - Valójában nem tudja futtatni
- 🔍 **Megoldás**: Explicit dokumentáció review + valós futtatás

### Illustration image creation prompt

Create an illustration showing an AI writing documentation with imaginary features floating in thought bubbles (dropdowns, real-time updates, advanced features) that don't exist in the actual code below. Show a developer reading the docs with a confused expression. Include a "reality check" stamp or magnifying glass examining the discrepancy. Use contrasting colors for imaginary vs. real.

### Comments for the presenter

Ez az egyik **legveszélyesebb hallucináció típus**, mert a dokumentáció úgy néz ki, mintha helyes lenne.

**Konkrét eset 1 - ProjectLabAdmin:**
tanulsagok.txt-ből Kristóf észrevétele:
```
"Planner xlsx leírásában masszív hallucinálás:
'4. **Manual Session Planning**
   - Open session_planner.xlsx
   - Use dropdown menus to assign students to slots
   - Monitor real-time statistics updates'

Nem is hallgatókat kell itt szekciókhoz rendelni és nincsen 
real-time update."
```

**Miért veszélyes**: Tipikusan ilyen feature-ökkel szokás reklámozni hasonló rendszereket, szóval az AI "kitalálta" őket.

**Konkrét eset 2 - SmartdocKitolto:**
```
"Készített a VBA scriptbe egy teszt sub-ot és mondta, 
hogy most tesztelni fogja, pedig nem is tudja futtatni. 
(Kézzel kitöröltem.)"
```

Az AI **szimulálta a futtatást** anélkül, hogy valóban végrehajtotta volna.

**Konkrét eset 3 - Stryker.NET HTML report:**
EViP_ZH_gen projektben:
```
Prompt: "Question: when you are reading the mutation testing reports, 
do you see the markings indicating the surviving mutations? 
Or are you just guessing based on the source code?"

Later: "Have a look at the webpage about reporters. Use JSON format 
instead."
```

Az AI azt állította, hogy látja a report részleteit, de valójában csak tippelt.

**Hogyan előzd meg:**

1. **Explicit dokumentáció review kérése**: "Please review the README and ensure all mentioned features actually exist in the code"

2. **Valós futtatás**: Ne higgy a szimulált output-nak, kérd meg hogy futtassa ténylegesen

3. **Cross-check**: Ha valami túl jónak tűnik, futtasd le személyesen

4. **Kérdezz vissza**: "Do you actually see the data or are you inferring from the code?"

## Slide 18: Összefoglalás - Mikor éri meg az AI?

### Title

ROI: Mikor nyerünk és mikor veszítünk időt?

### Content

- ✅ **Nagy nyereség** (5-10x gyorsabb):
  - Strukturált, jól definiált feladatok
  - Boilerplate kód, projekt struktúra
  - Refaktorálás, unit test generálás
- ⚠️ **Kicsi nyereség vagy semleges**:
  - PDF parsing (sok iteráció)
  - Komplex Selenium (edge case-ek)
- ❌ **Időbefektetés vagy veszteség**:
  - Tényfeltárás domain tudás nélkül
  - Hallucinált dokumentáció javítása

### Illustration image creation prompt

Create an ROI chart with three columns: Green "Big Wins" column showing rocket ship and 5-10x multiplier, yellow "Neutral" column showing balanced scales, and red "Time Loss" column showing stop sign and −1x. Include icons for different task types in each column. Use clear business metrics visualization style.

### Comments for the presenter

Ez a **végső összegző üzenet**: az AI nem mindenhol hatékony, de a megfelelő területeken hatalmas fejlesztési gyorsulást ad.

**Nagy nyereség területek:**

1. **Strukturált implementáció** - ahol a feladat egyértelmű:
   - API integráció known endpoint-okkal
   - Algoritmus implementáció specifikáció alapján
   - CRUD műveletek, form validation
   - **Sebesség**: 5-10x nem túlzás!

2. **Boilerplate és project setup**:
   - Python virtual env + requirements.txt
   - C# solution structure + project references
   - Unit test framework setup
   - Git ignore, README template

3. **Refaktorálás és kódminőség**:
   - SOLID principles alkalmazása
   - Code smell-ek felismerése
   - Duplicated code extraction
   - Naming convention javítás

4. **Mutation testing alapú javítás**:
   - Stryker.NET eredmények alapján hiányzó tesztek
   - Edge case-ek találása

**Kis nyereség vagy semleges:**

BillSummarizer tanulság:
```
"A PDF-ből adatkinyerés alapos tesztelést igényel. Pénzösszegben 
tizedesvessző, pont, szóköz bekavarnak. Elég sokat iterált az AI, 
de viszonylag magától."
```

Működik, de sok iteráció kell → nem sokkal gyorsabb mint manuális fejlesztés.

**Időbefektetés vagy veszteség:**

tanulsagok.txt-ből:
```
"A tényfeltárást igénylő feladatoknál, mint a PII kutatás, 
az AI használata gyakran inkább hátráltató tényező volt. 
A hallucinált adatok kiszűrése és a korrekciók néha több időt 
emésztettek fel, mintha manuálisan végeztem volna a kutatást. 
Az AI asszisztencia itt csak akkor hatékony, ha a fejlesztő 
már rendelkezik a validáláshoz szükséges domain-tudással."
```

**Végső üzenet**: 
"Az AI-asszisztált fejlesztés hatékonysága legnagyobb, ha mérnöki pontosságú, strukturált prompt-okat használunk, folyamatos validációt végzünk, és van domain tudásunk a feladat területén."

## Slide 19: Leckék és best practice-ek összefoglalva

### Title

Top 10 tanulság a projektekből

### Content

1. **Strukturált spec + feature kódok** 📋
2. **Iteratív fejlesztés** (Least-to-Most) 🔄
3. **Persona + megszorítások** explicit 👤
4. **Konkrét példák > elvont szabályok** 📝
5. **Acceptance Criteria használata** ✅
6. **Performance explicit optimalizálás** ⚡
7. **Encoding early agreement** 🔤
8. **InformationForAI.md jegyzetelés** 💾
9. **Human-in-the-loop folyamatos** 👁️
10. **Új chat ha lassul vagy regression** 🆕

### Illustration image creation prompt

Create a professional "top 10" infographic-style layout with numbered items 1-10, each with a small icon representing the concept. Use a clean, modern design with progressive colors from top to bottom. Include checkmarks and emphasis on key terms. Style should be suitable for a technical presentation closing slide.

### Comments for the presenter

Ez az **összefoglaló slide** az összes legfontosabb tanulságot gyors áttekintésben.

**Gyors átvétel minden pontról:**

1. **Strukturált spec + feature kódok**: "(DLXLS)", "(MKXLSX)" → egyértelmű hivatkozás
2. **Iteratív fejlesztés**: Ne egyszerre mindent, feladat feldarabolás
3. **Persona + megszorítások**: "Role: Senior Python engineer" + "no AI usage"
4. **Konkrét példák**: "38.1 expectednél legyen vonal, ±0.25 → 38.35 és 37.85"
5. **Acceptance Criteria**: AC1, AC2... pontosan mi a "kész"
6. **Performance**: Explicit kérés az optimalizációra, ne naiv implementáció
7. **Encoding**: UTF-8 minden, korai megbeszélés, következetesség
8. **InformationForAI.md**: Az AI jegyzeteljen magának gyors catch-up-hoz
9. **Human-in-the-loop**: Folyamatos validáció, főleg tényfeltárásnál
10. **Új chat**: Ha lassulás vagy regression → fresh start + InformationForAI.md

**Zárógondolat a diákoknak:**

Az AI nem varázspálca, hanem **power tool** - mint egy profi fűrész. Rossz technikával veszélyes és hatástalan. Jó technikával többszörösen gyorsít.

A közös pont minden tanulságban: **mérnöki gondolkodás + strukturáltság + validáció**. Ha ezeket kombináljuk az AI képességeivel, óriási produktivitás növekedést érhetünk el.

**Hangsúly**: Ne az AI-t hibáztassuk, ha nem jó az eredmény - 90%-ban a prompt minőségén múlik. A jó prompt írás **tanulható skill**, pont mint a clean code vagy a testing.

## Slide 20: Gyakorlati feladat

### Title

Próbáld ki Te is! - Mini projekt

### Content

- 🎯 **Feladat**: Excel makró adatgyűjtésre
  - Spec.md készítése feature kódokkal
  - Persona + AC-k használata
  - Iteratív implementáció
- 📝 **Dokumentáld**:
  - Hány iteráció kellett?
  - Milyen buktatók voltak?
  - Jegyzetelj prompts.md-be
- 💡 **Reflektálj**: mi működött, mi nem?

### Illustration image creation prompt

Create an encouraging illustration showing a student at a computer ready to start a project, with a checklist showing "Spec.md", "Feature codes", "Acceptance Criteria", "prompts.md". Include a lightbulb for ideas and a path forward. Use motivating, energetic colors like orange and blue.

### Comments for the presenter

Ez a **gyakorlati kitekintés**, hogy a diákok maguk is kipróbálhassák a tanultakat.

**Javasolt mini projekt specifikáció:**

**Cél**: Excel makró, ami egy adott könyvtárban lévő több Excel fájlból összegyűjti a "Sales" munkalapok tartalmát egy összesítő fájlba.

**Miért jó ez gyakorlatnak:**
- Elég egyszerű ahhoz, hogy 1-2 órában elkészüljön
- Elég komplex, hogy minden tanulságot alkalmazni lehessen
- VBA makró → tipikus enterprise automation task
- Valós használati eset

**Mit kell alkalmazni:**

1. **spec.md írása feature kódokkal**:
   ```
   (COLLECT) - Collect data from multiple files
   (MERGE) - Merge data into single sheet
   (VALIDATE) - Validate data consistency
   ```

2. **Persona és megszorítások**:
   - "Excel VBA macro for Excel 2016+"
   - "No external libraries"
   - "User-friendly error messages"

3. **Acceptance Criteria**:
   - AC1: Processes all .xlsx files in directory
   - AC2: Handles missing "Sales" sheet gracefully
   - AC3: Shows progress message
   - AC4: Completes on 50 files in <10 seconds

4. **Iteratív fejlesztés**:
   - 1. feature: csak fájlok listázása
   - 2. feature: egy fájl beolvasása
   - 3. feature: összes fájl összegyűjtése
   - 4. feature: error handling

5. **prompts.md dokumentálás**:
   - Minden prompt és az AI válasz összefoglalója
   - Buktatók, amikbe belefutottál
   - Hány iteráció kellett feature-enként

**Reflektálási kérdések a végén:**
- Mennyi időt spóroltál az AI-val vs. manuális kódolás?
- Hány hallucináció volt?
- Melyik prompt technika működött legjobban?
- Mit csinálnál másként legközelebb?

**Bónusz challenge**: Próbálj meg ugyanezt a specifikációt adni **nulla feature kód, nulla AC, nulla persona** nélkül → lásd a különbséget!
