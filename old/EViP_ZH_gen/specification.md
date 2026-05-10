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

**Helye:** `LogAnalyzer.Tests\BasicTestSetupTests.cs`

Hozza létre a tesztelési alapstruktúrát:
- `LogAnalyzerServiceTests` osztály létrehozása
- Test setup konstruktor implementálása teszt adatokkal
- Alapvető `LogAnalyzerService` példány létrehozása
- 5 különböző típusú teszt `LogEntry` létrehozása a teszteléshez

**Átadandó tesztek ebben a lépésben:**
- `LogAnalyzerService_CanBeInstantiated()`
- `TestData_ContainsFiveDifferentEntries()`
- `TestData_ContainsDifferentUsers()`
- `TestData_ContainsEmailAndIPInMessages()`
- `LogEntry_Properties_CanBeSetAndRetrieved()`
- `LogEntry_DefaultValues_AreEmptyStrings()`
- `LogAnalyzerService_PublicMethods_AreAvailable()`
- `TestSetup_ValidatesBasicFunctionality()`

**Célzott tesztek száma:** 8 alapvető teszt

### 7.2 Fájlkezelési tesztek implementálása

**Helye:** `LogAnalyzer.Tests\FileHandlingTests.cs`

Készítsen teszteket a fájl I/O műveletek minden lehetséges forgatókönyvére:
- **Érvényes fájl beolvasása:** `ReadLogFile_ValidFile_ReturnsCorrectEntries()`
- **Nem létező fájl kezelése:** `ReadLogFile_NonExistentFile_ThrowsFileNotFoundException()`
- **Üres fájl kezelése:** `ReadLogFile_EmptyFile_ReturnsEmptyList()`
- **Csak hibás bejegyzéseket tartalmazó fájl:** `ReadLogFile_FileWithOnlyInvalidEntries_ReturnsEmptyList()`
- **Vegyes érvényes/érvénytelen bejegyzések:** `ReadLogFile_FileWithMixedValidAndInvalidEntries_ReturnsOnlyValidEntries()`

**Átadandó tesztek ebben a lépésben:**
- `ReadLogFile_ValidFile_ReturnsCorrectEntries()`
- `ReadLogFile_NonExistentFile_ThrowsFileNotFoundException()`
- `ReadLogFile_EmptyFile_ReturnsEmptyList()`
- `ReadLogFile_FileWithOnlyInvalidEntries_ReturnsEmptyList()`
- `ReadLogFile_FileWithMixedValidAndInvalidEntries_ReturnsOnlyValidEntries()`
- `ReadLogFile_LargeFile_PerformsReasonably()`

**Tipp:** Használjon `Path.GetTempFileName()` és `File.WriteAllText()` metódusokat ideiglenes tesztfájlok létrehozásához.

**Célzott tesztek száma:** 6 fájlkezelési teszt

### 7.3 Formátum validálási tesztek kifejlesztése

**Helye:** `LogAnalyzer.Tests\FormatValidationTests.cs`

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

**Átadandó tesztek ebben a lépésben:**
- `IsValidLogFormat_ValidFormat_ReturnsTrue()`
- `IsValidLogFormat_InvalidFormat_ReturnsFalse()`
- `IsValidLogFormat_NullAndEmptyString_ReturnsFalse()`
- `IsValidLogFormat_VariousValidFormats_ReturnsTrue()` (Theory teszt - 5 eset)
- `IsValidLogFormat_InvalidDateTimeFormats_ReturnsFalse()` (Theory teszt - 6 eset)
- `IsValidLogFormat_InvalidLogLevels_ReturnsFalse()` (Theory teszt - 4 eset)
- `IsValidLogFormat_EmptyUser_ReturnsFalse()`
- `IsValidLogFormat_EmptyMessage_ReturnsFalse()`
- `IsValidLogFormat_MissingBrackets_ReturnsFalse()`
- `IsValidLogFormat_ValidLogLevels_ReturnsTrue()`
- `IsValidLogFormat_UsernameWithSpecialCharacters_ReturnsTrue()`

**Tipp:** A dátum validáláshoz használjon `DateTime.TryParseExact()` metódust a regex után.

**Célzott tesztek száma:** 11 validálási teszt

### 7.4 Szűrési és számolási tesztek

**Helye:** `LogAnalyzer.Tests\FilteringAndCountingTests.cs`

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

**Átadandó tesztek ebben a lépésben:**
- `FilterByLevel_WithValidLevel_ReturnsCorrectEntries()`
- `FilterByLevel_CaseInsensitive_ReturnsCorrectEntries()`
- `FilterByLevel_NonExistentLevel_ReturnsEmpty()`
- `FilterByLevel_EmptyLevel_ReturnsEmpty()`
- `FilterByLevel_NullLevel_ReturnsEmpty()`
- `FilterByLevel_EmptyEntries_ReturnsEmpty()`
- `FilterByLevel_WhitespaceLevel_ReturnsEmpty()`
- `FilterByLevel_NullEntries_ThrowsException()`
- `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()`
- `CountErrorEntries_WithNoErrorEntries_ReturnsZero()`
- `CountErrorEntries_EmptyList_ReturnsZero()`
- `CountErrorEntries_CaseInsensitive_ReturnsCorrectCount()`
- `CountErrorEntries_WithNullEntries_ThrowsException()`
- `CountErrorEntries_LargeDataset_PerformsWell()`
- `CountErrorEntries_OnlyErrorEntries_ReturnsTotal()`

**Célzott tesztek száma:** 15 szűrési/számolási teszt

### 7.5 Felhasználói aktivitás elemzési tesztek

**Helye:** `LogAnalyzer.Tests\UserActivityAnalysisTests.cs`

Implementáljon teszteket a felhasználói aktivitás összegzésére:
- **Alapvető aktivitás összegzés:** `GetUserActivitySummary_ReturnsCorrectCounts()`
- **Üres és null felhasználók kizárása:** `GetUserActivitySummary_EntriesWithEmptyUsers_ExcludesEmptyUsers()`
- **Duplikált felhasználók kezelése:** `GetUserActivitySummary_DuplicateUsers_CountsCorrectly()`
- **Null paraméter exception:** Megfelelő `ArgumentNullException` dobása

**Átadandó tesztek ebben a lépésben:**
- `GetUserActivitySummary_ReturnsCorrectCounts()`
- `GetUserActivitySummary_EmptyList_ReturnsEmptyDictionary()`
- `GetUserActivitySummary_EntriesWithEmptyUsers_ExcludesEmptyUsers()`
- `GetUserActivitySummary_DuplicateUsers_CountsCorrectly()`
- `GetUserActivitySummary_WithNullEntries_ThrowsException()`
- `GetUserActivitySummary_LargeDataset_PerformsWell()`
- `GetUserActivitySummary_CaseSensitiveUsers_TreatsAsDistinct()`
- `GetUserActivitySummary_SingleUser_ReturnsCorrectCount()`

**Célzott tesztek száma:** 8 aktivitás elemzési teszt

### 7.6 E-mail extrakciós tesztek kifejlesztése

**Helye:** `LogAnalyzer.Tests\EmailExtractionTests.cs`

Készítsen átfogó teszteket az e-mail címek kinyerésére:

#### 7.6.1 Alapvető e-mail extrakció
- **Érvényes e-mailek felismerése:** `ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()`
- **Duplikált e-mailek kezelése:** `ExtractEmailAddresses_WithDuplicateEmails_ReturnsUniqueEmails()`
- **E-mail nélküli szövegek:** `ExtractEmailAddresses_WithNoEmails_ReturnsEmptyList()`

#### 7.6.2 E-mail formátum validálás Theory tesztekkel
- **Különböző érvényes formátumok:** `ExtractEmailAddresses_VariousValidFormats_ExtractsCorrectly()`
- **Hibás formátumok elutasítása:** `ExtractEmailAddresses_InvalidFormats_DoesNotExtract()`
- **Több e-mail egy üzenetben:** `ExtractEmailAddresses_MultipleEmailsInOneMessage_ExtractsAll()`

**Átadandó tesztek ebben a lépésben:**
- `ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()`
- `ExtractEmailAddresses_WithNoEmails_ReturnsEmptyList()`
- `ExtractEmailAddresses_WithDuplicateEmails_ReturnsUniqueEmails()`
- `ExtractEmailAddresses_VariousValidFormats_ExtractsCorrectly()` (Theory teszt - 5 eset)
- `ExtractEmailAddresses_InvalidFormats_DoesNotExtract()` (Theory teszt - 6 eset)
- `ExtractEmailAddresses_MultipleEmailsInOneMessage_ExtractsAll()`
- `ExtractEmailAddresses_EmptyList_ReturnsEmptyList()`
- `ExtractEmailAddresses_WithNullEntries_ThrowsException()`
- `ExtractEmailAddresses_WithSpecialCharactersInEmails_ExtractsCorrectly()`
- `ExtractEmailAddresses_LargeDataset_PerformsWell()`
- `ExtractEmailAddresses_ComplexEmailFormats_ExtractsCorrectly()`

**Tipp:** Fejlesszen ki egy `IsValidEmailStructure()` privát metódust a részletes e-mail validáláshoz.

**Célzott tesztek száma:** 11 e-mail extrakciós teszt

### 7.7 IP cím extrakciós tesztek implementálása

**Helye:** `LogAnalyzer.Tests\IPAddressExtractionTests.cs`

Hozzon létre részletes teszteket az IP címek kinyerésére:

#### 7.7.1 Alapvető IP extrakció
- **Érvényes IP-k felismerése:** `ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()`
- **Hibás IP-k kiszűrése:** `ExtractIPAddresses_WithInvalidIPs_FiltersCorrectly()`
- **Duplikált IP-k kezelése:** `ExtractIPAddresses_WithDuplicateIPs_ReturnsUniqueIPs()`

#### 7.7.2 IP validálás szélsőséges esetek
- **Különböző érvényes IP formátumok:** `ExtractIPAddresses_VariousValidIPs_ExtractsCorrectly()`
- **Hibás formátumok elutasítása:** `ExtractIPAddresses_InvalidFormats_DoesNotExtract()`
- **Határérték validálás:** 0-255 közötti értékek ellenőrzése minden oktetben

**Átadandó tesztek ebben a lépésben:**
- `ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()`
- `ExtractIPAddresses_WithNoIPs_ReturnsEmptyList()`
- `ExtractIPAddresses_WithInvalidIPs_FiltersCorrectly()`
- `ExtractIPAddresses_VariousValidIPs_ExtractsCorrectly()` (Theory teszt - 7 eset)
- `ExtractIPAddresses_InvalidFormats_DoesNotExtract()` (Theory teszt - 8 eset)
- `ExtractIPAddresses_MultipleIPsInOneMessage_ExtractsAll()`
- `ExtractIPAddresses_WithDuplicateIPs_ReturnsUniqueIPs()`
- `ExtractIPAddresses_EmptyList_ReturnsEmptyList()`
- `ExtractIPAddresses_WithNullEntries_ThrowsException()`
- `ExtractIPAddresses_PrivateIPRanges_ExtractsCorrectly()`
- `ExtractIPAddresses_LargeDataset_PerformsWell()`
- `ExtractIPAddresses_BoundaryValues_HandlesCorrectly()`
- `ExtractIPAddresses_AllValidIPPatterns_ExtractsCorrectly()`

**Tipp:** Implementáljon egy `IsValidIPAddress()` privát metódust, amely ellenőrzi, hogy minden oktet 0-255 között van-e.

**Célzott tesztek száma:** 13 IP extrakciós teszt

### 7.8 Szélsőséges esetek és integrációs tesztek implementálása

**Helye:** `LogAnalyzer.Tests\EdgeCasesAndIntegrationTests.cs`

Hozzon létre teljeskörű integrációs teszteket és szélsőséges eseteket:

#### 7.8.1 Integrációs tesztek
- **Teljes munkamenet:** Fájl beolvasástól az összes adattranszformációig
- **Többszálú működés:** Thread safety validálás
- **Memória hatékonyság:** Nagy adatok kezelése

#### 7.8.2 Szélsőséges esetek
- **Üres fájlok kezelése:** Null vagy üres bemenetek
- **Nem várt formátumok:** Hibás vagy szokatlan log bejegyzések
- **Teljesítmény tesztek:** Nagy adatkészleteken való működés

**Átadandó tesztek ebben a lépésben:**
- `FullWorkflow_CompleteLogFile_ProcessesCorrectly()`
- `ConcurrentAccess_MultipleThreads_ThreadSafe()`
- `LargeDataset_ThousandsOfEntries_HandlesEfficiently()`
- `MemoryUsage_LargeDataset_DoesNotExceedLimits()`
- `EmptyFile_HandlesGracefully()`
- `MalformedEntries_SkipsAndContinues()`
- `SpecialCharacters_InLogMessages_HandledCorrectly()`
- `MultipleFilters_CombinedOperations_ProducesCorrectResults()`

**Célzott tesztek száma:** 8 integráció/szélsőséges eset teszt

---

## 8. Tesztek futtatása

Az összes teszt futtatásához használja a következő parancsot a projekt gyökerében:

```bash
dotnet test
```

Egy adott teszt osztály futtatásához:

```bash
dotnet test --filter "ClassName=BasicTestSetupTests"
```

Egy specifikus teszt futtatásához:

```bash
dotnet test --filter "FullyQualifiedName~ReadLogFile_ValidFile_ReturnsCorrectEntries"
```

---

## 9. Értékelési kritériumok

**Teljes pontszám:** 100 pont

- **7.1 Alapvető tesztelési setup (10 pont):** 8 teszt átadása
- **7.2 Fájlkezelési tesztek (15 pont):** 6 teszt átadása
- **7.3 Formátum validációs tesztek (15 pont):** 11 teszt átadása  
- **7.4 Szűrési és számlálási tesztek (20 pont):** 15 teszt átadása
- **7.5 Felhasználói aktivitás elemzési tesztek (15 pont):** 8 teszt átadása
- **7.6 Email extrakciós tesztek (15 pont):** 11 teszt átadása
- **7.7 IP cím extrakciós tesztek (15 pont):** 13 teszt átadása
- **7.8 Szélsőséges esetek és integrációs tesztek (10 pont):** 8 teszt átadása

**Részpontszámok:** Minden részfeladat tesztjeinek arányos teljesítése alapján.

**Sikeres vizsga:** Minimum 60 pont elérése (legalább 60% teszt sikeres átadása).

---

## 10. Hasznos tippek

1. **Inkrementális fejlesztés:** Kezdje az alap tesztekkel és fokozatosan haladjon
2. **Hibaüzenetek olvasása:** A tesztek világos hibaüzeneteket adnak
3. **Kód újrafelhasználás:** A közös logikát emelt ki privát metódusokba
4. **Tesztelési minták:** Figylje meg a Theory és InlineData használatát
5. **Teljesítmény:** Nagy adatkészleteken is hatékonyan működjön a kód

**Jó szerencsét a vizsgához!**
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
- 200+ átfogó teszt 100%-os sikerességgel (elért: 218 teszt)
- Minden publikus metódus teljes lefedettséggel
- Szélsőséges esetek (null, empty, invalid input) kezelése
- Teljesítmény validálás nagy adatkészletekkel  
- Robusztus validáció (datetime, email, IP cím formátumok)
- Átfogó dokumentáció és példák
- **Bónusz:** Mutációs tesztelés 75%+ pontszámmal (elért: 77.67%)

**Értékelési súlyok:**
- Funkcionális implementáció (40%)
- Tesztelési lefedettség és minőség (35%) 
- Kód minőség és struktúra (15%)
- Dokumentáció és használhatóság (10%)

**Sikerességi kritériumok:**
- ✅ Minden projekt lefordul hiba nélkül
- ✅ Konzol alkalmazás minden funkcióval működik
- ✅ 200+ átfogó teszt 100%-os pass rate-tel (túlteljesített: 218 teszt)
- ✅ Teljesítmény tesztek megfelelő eredménnyel
- ✅ Átfogó dokumentáció elkészült
- ✅ **Bónusz:** 77.67% mutációs tesztelési pontszám (Stryker.NET)

---

## 9. Haladó tesztelési technikák: Mutációs tesztelés (Bónusz)

**Helye:** Projekt gyökér könyvtár

### 9.1 Stryker.NET Mutációs Tesztelés Beállítása

A mutációs tesztelés a tesztek minőségének értékelésére szolgáló technika, amely a forráskódban apró változtatásokat (mutációkat) hajt végre, és ellenőrzi, hogy a tesztek képesek-e ezeket a hibákat felismerni.

#### 9.1.1 Stryker.NET Telepítése
```bash
# Eszköz manifest létrehozása (ha még nem létezik)
dotnet new tool-manifest

# Stryker.NET telepítése helyi eszközként
dotnet tool install dotnet-stryker

# Futtatás a teszt projekt könyvtárból
cd LogAnalyzer.Tests
dotnet stryker
```

#### 9.1.2 Mutációs Tesztelés Alapjai
A Stryker.NET a következő típusú mutációkat végzi:
- **Logikai operátorok:** `&&` ↔ `||`, `!` eltávolítása
- **Összehasonlító operátorok:** `>` ↔ `>=`, `==` ↔ `!=`
- **Aritmetikai operátorok:** `+` ↔ `-`, `*` ↔ `/`
- **Return értékek:** `true` ↔ `false`, számok megváltoztatása
- **String literálok:** üres stringre vagy nullra cserélés

### 9.2 Célzott Mutáció-Ellenes Tesztek

A magas mutációs pontszám eléréséhez készítsen célzott teszteket:

#### 9.2.1 Kivétel üzenet validálás
```csharp
[Fact]
public void ReadLogFile_FileNotFound_ThrowsWithSpecificMessage()
{
    // Ez megakadályozza a kivétel üzenet mutációkat
    var exception = Assert.Throws<FileNotFoundException>(() => 
        _service.ReadLogFile("nonexistent.log"));
    Assert.Contains("Log file not found:", exception.Message);
    Assert.NotEqual("", exception.Message); // Üres string mutáció ellen
}
```

#### 9.2.2 Logikai operátor tesztek
```csharp
[Theory]
[InlineData("user@")] // Teszteli: email.EndsWith("@") feltételt
[InlineData("@domain.com")] // Teszteli: email.StartsWith("@") feltételt
public void ExtractEmailAddresses_InvalidFormats_RejectsCorrectly(string invalidEmail)
{
    // Ez megakadályozza a || -> && mutációkat
    var result = _service.ExtractEmailAddresses(CreateTestEntries(invalidEmail));
    Assert.Empty(result);
}
```

#### 9.2.3 Határérték tesztek
```csharp
[Theory]
[InlineData("255.255.255.255", true)]  // Felső határ
[InlineData("255.255.255.256", false)] // Túllépés
[InlineData("0.0.0.0", true)]         // Alsó határ
[InlineData("-1.0.0.0", false)]       // Alullépés
public void IsValidIPAddress_BoundaryValues_HandlesCorrectly(string ip, bool expected)
{
    // Ez megakadályozza a >= -> > és <= -> < mutációkat
    Assert.Equal(expected, _service.IsValidIPAddress(ip));
}
```

### 9.3 Mutációs Tesztelés Célértékek

#### 9.3.1 Reális Célértékek
- **Kezdő szint:** 70-75% mutációs pontszám
- **Haladó szint:** 75-85% mutációs pontszám  
- **Szakértő szint:** 85%+ mutációs pontszám

#### 9.3.2 Mutációs Pontszám Értelmezése
```
Mutation Score = (Killed Mutations / Total Mutations) × 100%

Például: 78 killed + 14 survived = 92 total
Mutation Score = (78 / 92) × 100% = 84.78%
```

### 9.4 Mutációs Tesztelés Eredmények Értékelése

#### 9.4.1 Túlélő Mutációk Elemzése
A túlélő mutációk gyakori típusai és megoldásaik:

1. **Statement eltávolítás mutációk**
   - Probléma: `return result;` → `;`
   - Megoldás: Ellenőrizze a visszatérési értékek típusát és tartományát

2. **Logikai operátor mutációk**
   - Probléma: `if (A || B)` → `if (A && B)`
   - Megoldás: Tesztelje minden feltételt külön-külön

3. **String literál mutációk**
   - Probléma: `"."` → `""`
   - Megoldás: Ellenőrizze a string konstansok használatát

#### 9.4.2 Javítási Stratégiák
```csharp
// Rossz: Nem teszteli minden esetet
Assert.True(result.Count > 0);

// Jó: Specifikus értéket ellenőriz
Assert.Equal(3, result.Count);
Assert.Contains("expected@email.com", result);
```

### 9.5 Bónusz Pontszerzés

**Mutációs tesztelés eredményei alapján:**
- **75-80% mutációs pontszám:** +5 bónusz pont
- **80-85% mutációs pontszám:** +10 bónusz pont  
- **85%+ mutációs pontszám:** +15 bónusz pont

**Dokumentáció bónusz:** +5 pont a mutációs tesztelés eredményeinek elemzéséért

---

## 10. Fejlett Tesztelési Minták (Opcionális)

### 10.1 Property-Based Testing
```csharp
// FsCheck vagy Hedgehog.NET használatával
[Property]
public bool ExtractIPAddresses_ValidIPs_AlwaysExtracted(ValidIPAddress ip)
{
    var entries = CreateTestEntries(ip.Value);
    var result = _service.ExtractIPAddresses(entries);
    return result.Contains(ip.Value);
}
```

### 10.2 Benchmark Tesztek
```csharp
[Fact]
public void ExtractEmailAddresses_LargeDataset_MeetsPerformanceRequirements()
{
    var largeDataset = GenerateEntries(10000);
    var stopwatch = Stopwatch.StartNew();
    
    var result = _service.ExtractEmailAddresses(largeDataset);
    
    stopwatch.Stop();
    Assert.True(stopwatch.ElapsedMilliseconds < 1000, 
        $"Expected < 1000ms, actual: {stopwatch.ElapsedMilliseconds}ms");
}
```

---

