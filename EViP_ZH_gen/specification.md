# Vizsgafeladat az EViP kurzushoz

Ez a megoldás egy vizsgafeladat mintamegvalósítását tartalmazza, amely naplófájlok elemzésével foglalkozik.
A vizsga alapvető C# szintaxisra, IEnumerable, LINQ, reguláris kifejezések és xUnit tesztelésre fókuszál.
A hallgatóknak a megoldást a nulláról kell elkészíteniük. A megoldásnak 3 projektet kell tartalmaznia: egy osztálykönyvtárat, egy konzol alkalmazást és egy teszt projektet. Mind a konzol alkalmazás, mind a teszt projekt hivatkozni fog az osztálykönyvtárra.

# Konkrét vizsgafeladat: Naplófájlok elemzése

A feladat célja, hogy a hallgatók egy naplófájlokat elemző rendszert készítsenek, amely a következő részfeladatokat tartalmazza:

## 1. Projekt struktúra létrehozása

**Helye:** Megoldás gyökér mappája

Hozza létre a következő projekt struktúrát:
- `LogAnalyzer.Core` - Class Library (.NET 8) projekt az üzleti logikához
- `LogAnalyzer.Console` - Console Application (.NET 8) projekt a felhasználói felülethez
- `LogAnalyzer.Tests` - Class Library (.NET 8) projekt a tesztekhez (xUnit referenciával)

Állítsa be a projekt referenciákat:
- `LogAnalyzer.Console` hivatkozzon a `LogAnalyzer.Core` projektre
- `LogAnalyzer.Tests` hivatkozzon a `LogAnalyzer.Core` projektre

## 2. Naplóbejegyzés modell és szolgáltatás létrehozása

**Helye:** `LogAnalyzer.Core` projekt

Hozza létre a következő osztályokat:

### 2.1 LogEntry modell
Készítsen egy `LogEntry` osztályt a következő tulajdonságokkal:
- `string Timestamp` - A naplóbejegyzés időpontja szöveg formátumban
- `string Level` - A napló szintje (INFO, WARNING, ERROR, DEBUG)
- `string Message` - A naplóüzenet
- `string User` - A felhasználó neve (opcionális)

### 2.2 LogAnalyzerService osztály
Hozza létre a `LogAnalyzerService` osztályt a következő metódusokkal:
- `List<LogEntry> ReadLogFile(string filePath)`
- `IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)`
- `int CountErrorEntries(IEnumerable<LogEntry> entries)`
- `Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)`
- `bool IsValidLogFormat(string logLine)`
- `List<string> ExtractEmailAddresses(IEnumerable<LogEntry> entries)`
- `List<string> ExtractIPAddresses(IEnumerable<LogEntry> entries)`

## 3. Naplófájl beolvasása és formátum validálása

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

### 3.1 Fájl beolvasása
Implementálja a `ReadLogFile` metódust, amely:
- Beolvassa a naplófájlt soronként
- Minden sort feldolgoz és létrehozza a `LogEntry` objektumokat
- Képes kezelni a következő formátumot: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message`
- Például: `[2024-01-15 10:30:45] [ERROR] [john.doe] Database connection failed`
- Hibakezelést tartalmaz nem létező fájl esetén

### 3.2 Formátum validálás reguláris kifejezéssel
Implementálja az `IsValidLogFormat` metódust, amely:
- Reguláris kifejezést használ a naplósor formátumának ellenőrzésére
- Ellenőrizze, hogy a sor a várt formátumban van-e: szögletes zárójelekben dátum és idő, majd szögletes zárójelekben a napló szint, majd szögletes zárójelekben a felhasználónév, végül az üzenet
- **Tipp:** Gondoljon a szögletes zárójelekre, számjegyekre, kötőjelekre, kettőspontokra és a négy lehetséges napló szintre
- Visszaadja, hogy a sor megfelel-e a várt formátumnak

## 4. Naplóbejegyzések szűrése és elemzése

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

### 4.1 Szint alapú szűrés
Implementálja a `FilterByLevel` metódust, amely:
- LINQ Where() metódussal szűri az adott szintű bejegyzéseket
- Case-insensitive összehasonlítást használ

### 4.2 Hibák számolása
Implementálja a `CountErrorEntries` metódust, amely:
- LINQ Count() metódussal számolja meg az ERROR szintű bejegyzéseket
- Case-insensitive összehasonlítást használ

### 4.3 Felhasználói aktivitás elemzése
Implementálja a `GetUserActivitySummary` metódust, amely:
- LINQ GroupBy és ToDictionary használatával csoportosítja a bejegyzéseket felhasználók szerint
- Visszaadja, hogy melyik felhasználó hány bejegyzést hozott létre

## 5. Reguláris kifejezések alkalmazása adatkinyeréshez

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

### 5.1 E-mail címek kinyerése
Implementálja az `ExtractEmailAddresses` metódust, amely:
- Reguláris kifejezést használ e-mail címek megtalálásához a naplóüzenetekben
- **Példa e-mail címek a naplóban:** `john.doe@company.com`, `support@website.hu`, `admin_user@test-site.org`
- **Tipp:** Az e-mail cím általában betűkből, számokból és bizonyos speciális karakterekből áll, majd egy @ jel, majd újra betűk/számok, egy pont, és végül a domain végződés
- LINQ SelectMany és Distinct használatával adja vissza az egyedi e-mail címeket

### 5.2 IP címek kinyerése
Implementálja az `ExtractIPAddresses` metódust, amely:
- Reguláris kifejezést használ IPv4 címek megtalálásához a naplóüzenetekben
- **Példa IP címek a naplóban:** `192.168.1.100`, `10.0.0.5`, `172.16.254.1`
- **Tipp:** IPv4 cím 4 db 0-255 közötti számból áll, pontokkal elválasztva. Gondoljon arra, hogy egy-egy szám 1-3 jegyű lehet
- LINQ SelectMany és Distinct használatával adja vissza az egyedi IP címeket

## 6. Konzol alkalmazás készítése

**Helye:** `LogAnalyzer.Console` projekt, `Program.cs`

Készítsen egy interaktív konzol alkalmazást, amely:
- Menü alapú navigációt biztosít
- Létrehoz egy `LogAnalyzerService` példányt a Main metódusban
- A következő funkciókat kínálja:
  1. Naplófájl betöltése
  2. Összes bejegyzés megjelenítése
  3. Adott szintű bejegyzések szűrése
  4. Hibák számának megjelenítése
  5. Felhasználói aktivitás összesítő
  6. E-mail címek kinyerése
  7. IP címek kinyerése
  8. Kilépés

Használjon egyszerű objektum-létrehozást (new kulcsszó) a szolgáltatás példányosításához.

## 7. Átfogó tesztelési rendszer fejlesztése

**Helye:** `LogAnalyzer.Tests` projekt

Készítsen egy átfogó tesztkészletet, amely minden funkciót és szélsőséges esetet lefed. A tesztek fokozatosan épüljenek fel a következő altevékenységek szerint:

### 7.1 Alapvető tesztelési környezet beállítása

**Helye:** `LogAnalyzer.Tests\UnitTest1.cs`

Hozza létre a tesztelési alapstruktúrát:
- `LogAnalyzerServiceTests` osztály létrehozása
- Test setup konstruktor implementálása teszt adatokkal
- Alapvető `LogAnalyzerService` példány létrehozása
- 5 különböző típusú teszt `LogEntry` létrehozása a teszteléshez

**Célzott tesztek száma:** 5-8 alapvető teszt

### 7.2 Fájlkezelési tesztek implementálása

Készítsen teszteket a fájl I/O műveletek minden lehetséges forgatókönyvére:
- **Érvényes fájl beolvasása:** `ReadLogFile_ValidFile_ReturnsCorrectEntries()`
- **Nem létező fájl kezelése:** `ReadLogFile_NonExistentFile_ThrowsFileNotFoundException()`
- **Üres fájl kezelése:** `ReadLogFile_EmptyFile_ReturnsEmptyList()`
- **Csak hibás bejegyzéseket tartalmazó fájl:** `ReadLogFile_FileWithOnlyInvalidEntries_ReturnsEmptyList()`
- **Vegyes érvényes/érvénytelen bejegyzések:** `ReadLogFile_FileWithMixedValidAndInvalidEntries_ReturnsOnlyValidEntries()`

**Tipp:** Használjon `Path.GetTempFileName()` és `File.WriteAllText()` metódusokat ideiglenes tesztfájlok létrehozásához.

**Célzott tesztek száma:** 5-6 fájlkezelési teszt

### 7.3 Formátum validálási tesztek kifejlesztése

Implementáljon részletes teszteket a formátum validáláshoz:

#### 7.3.1 Alapvető formátum tesztek
- **Érvényes formátum felismerése:** `IsValidLogFormat_ValidFormat_ReturnsTrue()`
- **Érvénytelen formátumok elutasítása:** `IsValidLogFormat_InvalidFormat_ReturnsFalse()`
- **Null és üres string kezelése:** Megfelelő hibakezelés tesztelése

#### 7.3.2 Paraméteres tesztek Theory attribútummal
Használjon `[Theory]` és `[InlineData]` attribútumokat:
- **Különböző érvényes formátumok:** `IsValidLogFormat_VariousValidFormats_ReturnsTrue()`
- **Hibás dátum formátumok:** `IsValidLogFormat_InvalidDateTimeFormats_ReturnsFalse()`
- **Hibás log szintek:** `IsValidLogFormat_InvalidLogLevels_ReturnsFalse()`

**Tipp:** A dátum validáláshoz használjon `DateTime.TryParseExact()` metódust a regex után.

**Célzott tesztek száma:** 8-12 validálási teszt

### 7.4 Szűrési és számolási tesztek

Készítsen teszteket minden LINQ-alapú műveletre:

#### 7.4.1 Szint alapú szűrés tesztelése
- **Érvényes szint szerinti szűrés:** `FilterByLevel_WithValidLevel_ReturnsCorrectEntries()`
- **Case-insensitive szűrés:** `FilterByLevel_CaseInsensitive_ReturnsCorrectEntries()`
- **Nem létező szint kezelése:** `FilterByLevel_NonExistentLevel_ReturnsEmpty()`
- **Null és üres paraméterek:** Hibakezelés tesztelése

#### 7.4.2 Error bejegyzések számolása
- **Hibák pontos számolása:** `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()`
- **Null paraméter kezelése:** `CountErrorEntries_WithNullEntries_ThrowsException()`
- **Case-insensitive számolás:** `CountErrorEntries_CaseInsensitive_ReturnsCorrectCount()`

**Célzott tesztek száma:** 10-12 szűrési/számolási teszt

### 7.5 Felhasználói aktivitás elemzési tesztek

Implementáljon teszteket a felhasználói aktivitás összegzésére:
- **Alapvető aktivitás összegzés:** `GetUserActivitySummary_ReturnsCorrectCounts()`
- **Üres és null felhasználók kizárása:** `GetUserActivitySummary_EntriesWithEmptyUsers_ExcludesEmptyUsers()`
- **Duplikált felhasználók kezelése:** `GetUserActivitySummary_DuplicateUsers_CountsCorrectly()`
- **Null paraméter exception:** Megfelelő `ArgumentNullException` dobása

**Célzott tesztek száma:** 5-6 aktivitás elemzési teszt

### 7.6 E-mail extrakciós tesztek kifejlesztése

Készítsen átfogó teszteket az e-mail címek kinyerésére:

#### 7.6.1 Alapvető e-mail extrakció
- **Érvényes e-mailek felismerése:** `ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()`
- **Duplikált e-mailek kezelése:** `ExtractEmailAddresses_WithDuplicateEmails_ReturnsUniqueEmails()`
- **E-mail nélküli szövegek:** `ExtractEmailAddresses_WithNoEmails_ReturnsEmptyList()`

#### 7.6.2 E-mail formátum validálás Theory tesztekkel
- **Különböző érvényes formátumok:** `ExtractEmailAddresses_VariousValidFormats_ExtractsCorrectly()`
- **Hibás formátumok elutasítása:** `ExtractEmailAddresses_InvalidFormats_DoesNotExtract()`
- **Több e-mail egy üzenetben:** `ExtractEmailAddresses_MultipleEmailsInOneMessage_ExtractsAll()`

**Tipp:** Fejlesszen ki egy `IsValidEmailStructure()` privát metódust a részletes e-mail validáláshoz.

**Célzott tesztek száma:** 12-15 e-mail extrakciós teszt

### 7.7 IP cím extrakciós tesztek implementálása

Hozzon létre részletes teszteket az IP címek kinyerésére:

#### 7.7.1 Alapvető IP extrakció
- **Érvényes IP-k felismerése:** `ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()`
- **Hibás IP-k kiszűrése:** `ExtractIPAddresses_WithInvalidIPs_FiltersCorrectly()`
- **Duplikált IP-k kezelése:** `ExtractIPAddresses_WithDuplicateIPs_ReturnsUniqueIPs()`

#### 7.7.2 IP validálás szélsőséges esetek
- **Különböző érvényes IP formátumok:** `ExtractIPAddresses_VariousValidIPs_ExtractsCorrectly()`
- **Hibás formátumok elutasítása:** `ExtractIPAddresses_InvalidFormats_DoesNotExtract()`
- **Verziószámok kizárása:** Ne kerüljenek bele az 1.2.3.4.5 típusú szövegek

**Tipp:** Implementáljon egy `IsValidIPAddress()` privát metódust, amely ellenőrzi, hogy minden oktet 0-255 között van-e.

**Célzott tesztek száma:** 12-15 IP extrakciós teszt

### 7.8 Szélsőséges esetek és integrációs tesztek

Fejlesszen ki teszteket a rendszer robusztusságának ellenőrzésére:

#### 7.8.1 Teljesítmény és nagyméretű adatok
- **Nagy adatkészletek kezelése:** `AllMethods_WithVeryLargeDataset_PerformReasonably()`
- **10,000+ bejegyzés feldolgozása:** Ellenőrizze, hogy a rendszer elfogadható időn belül működik

#### 7.8.2 Speciális karakterek és unicode
- **Speciális karakterek üzenetekben:** `ExtractMethods_WithSpecialCharactersInMessages_HandleCorrectly()`
- **Unicode karakterek kezelése:** Biztosítsa, hogy a rendszer kezeli a különleges karaktereket

#### 7.8.3 Thread safety alapvető tesztelése
- **Párhuzamos műveletek:** `AllMethods_ThreadSafety_BasicCheck()`
- **Concurrent hozzáférés:** Ellenőrizze, hogy a szolgáltatás biztonságosan használható párhuzamos környezetben

#### 7.8.4 LogEntry model tesztelése
- **Tulajdonságok beállítása:** `LogEntry_Properties_CanBeSetAndRetrieved()`
- **Alapértelmezett értékek:** `LogEntry_DefaultValues_AreEmptyStrings()`

**Célzott tesztek száma:** 6-8 integrációs teszt

### 7.9 Tesztelési best practices alkalmazása

Biztosítsa a következő tesztelési elvek betartását:

#### 7.9.1 Test szervezés
- **Regions használata:** Csoportosítsa a teszteket logikai régiókba
- **Konzisztens naming:** Használjon egyértelmű teszt neveket
- **Setup és cleanup:** Megfelelő erőforrás kezelés

#### 7.9.2 Assert minták
- **Több assertion egy tesztben:** Ahol indokolt, használjon több ellenőrzést
- **Exception tesztelés:** `Assert.Throws<T>()` használata
- **Collection assertions:** `Assert.Contains()`, `Assert.Empty()`, `Assert.All()` használata

#### 7.9.3 Test data management
- **Temporary file cleanup:** `try-finally` blokkok használata
- **Isolated tests:** Minden teszt legyen független
- **Meaningful test data:** Reális tesztadatok használata

**Összesen célzott tesztek száma: 75-85 átfogó teszt**

### 7.10 Tesztlefedettség validálása

A végső tesztkészletnek le kell fednie:
- ✅ **100% metódus lefedettség** - Minden publikus metódus tesztelt
- ✅ **Szélsőséges esetek** - Null, üres, hibás bemenetek
- ✅ **Pozitív és negatív forgatókönyvek** - Sikeres és sikertelen esetek
- ✅ **Performance validálás** - Nagy adatkészletek kezelése
- ✅ **Exception handling** - Megfelelő hibakezelés
- ✅ **Integration scenarios** - Komponensek együttműködése

**Várt eredmény:** 80+ teszt 100%-os sikerességi aránnyal

## 8. Mintafájl és dokumentáció

**Helye:** Megoldás gyökér mappája

### 8.1 Minta naplófájl
Hozzon létre egy `sample.log` fájlt legalább 20 sorral, amely tartalmaz:
- Különböző naplószinteket (INFO, WARNING, ERROR, DEBUG)
- Különböző felhasználókat
- E-mail címeket a naplóüzenetekben
- IP címeket a naplóüzenetekben
- Néhány hibás formátumú sort is a teszteléshez

Példa sorok:
```
[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity detected from 10.0.0.5
[2024-01-15 10:33:05] [DEBUG] [system] Email sent to support@company.hu successfully
Invalid log line without proper format
[2024-01-15 10:50:30] [INFO] [jane.smith] System maintenance scheduled
Another invalid line missing brackets and format
```

### 8.2 README.md és fejlett dokumentáció
Készítsen átfogó dokumentációt, amely tartalmazza:
- A projekt részletes leírását és célját
- Minden projekthez külön futtatási utasításokat
- A naplófájl formátumának részletes leírását példákkal
- A reguláris kifejezések alkalmazásának magyarázatát konkrét mintákkal
- Tesztelési stratégia dokumentálását
- A 80+ teszt kategorizálását és lefedettségét
- Teljesítmény tesztek eredményeinek összegzését
- Szélsőséges esetek kezelésének leírását
- Példákat a használatra és várt kimenetekre

### 8.3 Teszt lefedettség dokumentáció
Készítsen egy `test_coverage_summary.md` fájlt, amely tartalmazza:
- **Teszt statisztikák:** Összes teszt száma, sikeresség aránya
- **Kategorizálás:** 8 fő teszt kategória részletes lebontása
- **Szélsőséges esetek:** Lefedett edge case-ek listája
- **Teljesítmény eredmények:** Nagy adatkészlet tesztek eredményei
- **Validálási technikák:** Alkalmazott tesztelési minták
- **Robusztusság:** Null safety, hibakezelés, thread safety eredmények

## Értékelési szempontok

- **Kód minőség:** Clean code elvek betartása, megfelelő névadás
- **LINQ használat:** Hatékony és olvasható LINQ lekérdezések
- **Reguláris kifejezések:** Helyes regex minták létrehozása és alkalmazása
- **Átfogó tesztelés:** 75-85 teszt implementálása 100%-os sikerességgel
- **Szélsőséges esetek kezelése:** Edge case-ek és hibás bemenetek kezelése
- **Teljesítmény optimalizálás:** Nagy adatkészletek (10K+ entry) hatékony feldolgozása
- **Validálási robusztusság:** Strict datetime parsing, IP/email validálás
- **Hibakezelés:** Megfelelő exception handling és null safety
- **Projekt struktúra:** Tiszta kód szervezés, megfelelő felelősség megosztás
- **Test architektúra:** Regions, Theory tests, paraméteres tesztek használata
- **Dokumentáció minősége:** Részletes README és teszt lefedettség dokumentálás
- **Felhasználói élmény:** Intuitív konzol interfész minden funkcióval

## Határidő és leadás

A feladatot a vizsga időkeretén belül kell elkészíteni. A megoldásnak mind a három projektben futtathatónak és teszteltnek kell lennie.

**Minimális elvárások:**
- 75+ átfogó teszt 100%-os sikerességgel
- Minden publikus metódus teljes lefedettséggel
- Szélsőséges esetek (null, empty, invalid input) kezelése
- Teljesítmény validálás nagy adatkészletekkel  
- Robusztus validáció (datetime, email, IP cím formátumok)
- Átfogó dokumentáció és példák

**Értékelési súlyok:**
- Funkcionális implementáció (40%)
- Tesztelési lefedettség és minőség (35%) 
- Kód minőség és struktúra (15%)
- Dokumentáció és használhatóság (10%)

**Sikerességi kritériumok:**
- ✅ Minden projekt lefordul hiba nélkül
- ✅ Konzol alkalmazás minden funkcióval működik
- ✅ 75+ teszt 100%-os pass rate-tel
- ✅ Teljesítmény tesztek megfelelő eredménnyel
- ✅ Átfogó dokumentáció elkészült

