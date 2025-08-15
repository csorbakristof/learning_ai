# Vizsgafeladat az EViP kurzushoz

Ez a megoldás egy vizsgafeladat mintamegvalósítása, amely naplófájlok elemzésével foglalkozik.
A vizsga alapvetõ C# szintaxisra, IEnumerable, LINQ, és xUnit tesztelésre fókuszál.
A hallgatóknak a megoldást a nulláról kell elkészíteniük. A megoldásnak 3 projektet kell tartalmaznia: egy osztálykönyvtárat, egy konzol alkalmazást és egy teszt projektet. Mind a konzol alkalmazás, mind a teszt projekt hivatkozni fog az osztálykönyvtárra.

# Konkrét vizsgafeladat: Naplófájlok elemzése

A feladat célja, hogy a hallgatók egy naplófájlokat elemzõ rendszert készítsenek, amely a következõ részfeladatokat tartalmazza:

## 1. Projekt struktúra létrehozása

**Helye:** Megoldás gyökér mappája

Hozza létre a következõ projekt struktúrát:
- `LogAnalyzer.Core` - Class Library (.NET 8) projekt az üzleti logikához
- `LogAnalyzer.Console` - Console Application (.NET 8) projekt a felhasználói felülethez
- `LogAnalyzer.Tests` - Class Library (.NET 8) projekt a tesztekhez (xUnit referenciával)

Állítsa be a projekt referenciákat:
- `LogAnalyzer.Console` hivatkozzon a `LogAnalyzer.Core` projektre
- `LogAnalyzer.Tests` hivatkozzon a `LogAnalyzer.Core` projektre

## 2. Naplóbejegyzés modell és szolgáltatás létrehozása

**Helye:** `LogAnalyzer.Core` projekt

Hozza létre a következõ osztályokat:

### 2.1 LogEntry modell
Készítsen egy `LogEntry` osztályt a következõ tulajdonságokkal:
- `DateTime Timestamp` - A naplóbejegyzés idõpontja
- `string Level` - A napló szintje (INFO, WARNING, ERROR, DEBUG)
- `string Message` - A naplóüzenet
- `string User` - A felhasználó neve (opcionális)

### 2.2 ILogAnalyzerService interfész
Definiáljon egy interfészt a következõ metódusokkal:
- `Task<List<LogEntry>> ReadLogFileAsync(string filePath)`
- `IEnumerable<LogEntry> FilterByDate(IEnumerable<LogEntry> entries, DateTime date)`
- `int CountErrorEntries(IEnumerable<LogEntry> entries)`
- `Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)`
- `IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)`

### 2.3 LogAnalyzerService implementáció
Implementálja az `ILogAnalyzerService` interfészt LINQ használatával.

## 3. Naplófájl beolvasása és feldolgozása

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

Implementálja a `ReadLogFileAsync` metódust, amely:
- Aszinkron módon olvassa be a naplófájlt
- Feldolgozza a sorokat és létrehozza a `LogEntry` objektumokat
- Képes kezelni a következõ formátumot: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message`
- Például: `[2024-01-15 10:30:45] [ERROR] [john.doe] Database connection failed`
- Hibakezelést tartalmaz érvénytelen sorok esetén

## 4. Naplóbejegyzések szûrése és elemzése

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

### 4.1 Dátum alapú szûrés
Implementálja a `FilterByDate` metódust LINQ használatával, amely:
- Egy adott naphoz tartozó bejegyzéseket adja vissza
- Csak a dátumot veszi figyelembe, az idõt nem

### 4.2 Hibák számolása
Implementálja a `CountErrorEntries` metódust, amely:
- LINQ Count() metódussal számolja meg az ERROR szintû bejegyzéseket
- Case-insensitive összehasonlítást használ

### 4.3 Felhasználói aktivitás elemzése
Implementálja a `GetUserActivitySummary` metódust, amely:
- LINQ GroupBy és ToDictionary használatával csoportosítja a bejegyzéseket felhasználók szerint
- Visszaadja, hogy melyik felhasználó hány bejegyzést hozott létre

### 4.4 Szint alapú szûrés
Implementálja a `FilterByLevel` metódust, amely:
- Egy adott naplószinthez tartozó bejegyzéseket szûri ki
- Case-insensitive összehasonlítást használ

## 5. Konzol alkalmazás készítése

**Helye:** `LogAnalyzer.Console` projekt, `Program.cs`

Készítsen egy interaktív konzol alkalmazást, amely:
- Menü alapú navigációt biztosít
- Lehetõséget ad naplófájl megadására
- A következõ funkciókat kínálja:
  1. Naplófájl betöltése
  2. Összes bejegyzés megjelenítése
  3. Adott dátumhoz tartozó bejegyzések szûrése
  4. Hibák számának megjelenítése
  5. Felhasználói aktivitás összesítõ
  6. Adott szintû bejegyzések szûrése
  7. Kilépés

Használjon dependency injection-t az `ILogAnalyzerService` injektálásához.

## 6. Egységtesztek készítése

**Helye:** `LogAnalyzer.Tests` projekt

Hozzon létre legalább 5 tesztesetet xUnit keretrendszerrel:

### 6.1 LogAnalyzerServiceTests osztály
- `ReadLogFileAsync_ValidFile_ReturnsCorrectEntries()` - Érvényes fájl beolvasásának tesztelése
- `FilterByDate_ValidDate_ReturnsFilteredEntries()` - Dátum alapú szûrés tesztelése
- `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()` - Hibák számolásának tesztelése
- `GetUserActivitySummary_WithMultipleUsers_ReturnsCorrectSummary()` - Felhasználói aktivitás tesztelése
- `FilterByLevel_ValidLevel_ReturnsFilteredEntries()` - Szint alapú szûrés tesztelése

Használjon test data setup-ot és Assert metódusokat az eredmények ellenõrzésére.

## 7. Mintafájl és dokumentáció

**Helye:** Megoldás gyökér mappája

### 7.1 Minta naplófájl
Hozzon létre egy `sample.log` fájlt legalább 20 sorral, különbözõ:
- Dátumokkal
- Naplószintekkel (INFO, WARNING, ERROR, DEBUG)
- Felhasználókkal
- Üzenetekkel

### 7.2 README.md
Készítsen dokumentációt, amely tartalmazza:
- A projekt leírását
- Futtatási utasításokat
- A naplófájl formátumának leírását
- Példákat a használatra

## Értékelési szempontok

- **Kód minõség:** Clean code elvek betartása, megfelelõ névadás
- **LINQ használat:** Hatékony és olvasható LINQ lekérdezések
- **Aszinkron programozás:** Task és async/await helyes használata
- **Tesztelés:** Átfogó tesztlefedettség, jól strukturált tesztek
- **Hibakezelés:** Megfelelõ exception handling
- **Projekt struktúra:** Tiszta architektúra, megfelelõ separation of concerns
- **Felhasználói élmény:** Intuitív konzol interfész

## Határidõ és leadás

A feladatot a vizsga idõkeretén belül kell elkészíteni. A megoldásnak mind a három projektben futtathatónak és teszteltnek kell lennie.

