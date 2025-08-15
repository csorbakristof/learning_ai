# Vizsgafeladat az EViP kurzushoz

Ez a megoldás egy vizsgafeladat mintamegvalósítása, amely naplófájlok elemzésével foglalkozik.
A vizsga alapvetõ C# szintaxisra, IEnumerable, LINQ, reguláris kifejezések és xUnit tesztelésre fókuszál.
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
- `string Timestamp` - A naplóbejegyzés idõpontja szöveg formátumban
- `string Level` - A napló szintje (INFO, WARNING, ERROR, DEBUG)
- `string Message` - A naplóüzenet
- `string User` - A felhasználó neve (opcionális)

### 2.2 LogAnalyzerService osztály
Hozza létre a `LogAnalyzerService` osztályt a következõ metódusokkal:
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
- Képes kezelni a következõ formátumot: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message`
- Például: `[2024-01-15 10:30:45] [ERROR] [john.doe] Database connection failed`
- Hibakezelést tartalmaz nem létezõ fájl esetén

### 3.2 Formátum validálás reguláris kifejezéssel
Implementálja az `IsValidLogFormat` metódust, amely:
- Reguláris kifejezést használ a naplósor formátumának ellenõrzésére
- Ellenõrizze, hogy a sor a várt formátumban van-e: szögletes zárójelekben dátum és idõ, majd szögletes zárójelekben a napló szint, majd szögletes zárójelekben a felhasználónév, végül az üzenet
- **Tipp:** Gondoljon a szögletes zárójelekre, számjegyekre, kötõjelekre, kettõspontokra és a négy lehetséges napló szintre
- Visszaadja, hogy a sor megfelel-e a várt formátumnak

## 4. Naplóbejegyzések szûrése és elemzése

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` osztály

### 4.1 Szint alapú szûrés
Implementálja a `FilterByLevel` metódust, amely:
- LINQ Where() metódussal szûri az adott szintû bejegyzéseket
- Case-insensitive összehasonlítást használ

### 4.2 Hibák számolása
Implementálja a `CountErrorEntries` metódust, amely:
- LINQ Count() metódussal számolja meg az ERROR szintû bejegyzéseket
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
- **Tipp:** Az e-mail cím általában betûkbõl, számokból és bizonyos speciális karakterekbõl áll, majd egy @ jel, majd újra betûk/számok, egy pont, és végül a domain végzõdés
- LINQ SelectMany és Distinct használatával adja vissza az egyedi e-mail címeket

### 5.2 IP címek kinyerése
Implementálja az `ExtractIPAddresses` metódust, amely:
- Reguláris kifejezést használ IPv4 címek megtalálásához a naplóüzenetekben
- **Példa IP címek a naplóban:** `192.168.1.100`, `10.0.0.5`, `172.16.254.1`
- **Tipp:** IPv4 cím 4 db 0-255 közötti számból áll, pontokkal elválasztva. Gondoljon arra, hogy egy-egy szám 1-3 jegyû lehet
- LINQ SelectMany és Distinct használatával adja vissza az egyedi IP címeket

## 6. Konzol alkalmazás készítése

**Helye:** `LogAnalyzer.Console` projekt, `Program.cs`

Készítsen egy interaktív konzol alkalmazást, amely:
- Menü alapú navigációt biztosít
- Létrehoz egy `LogAnalyzerService` példányt a Main metódusban
- A következõ funkciókat kínálja:
  1. Naplófájl betöltése
  2. Összes bejegyzés megjelenítése
  3. Adott szintû bejegyzések szûrése
  4. Hibák számának megjelenítése
  5. Felhasználói aktivitás összesítõ
  6. E-mail címek kinyerése
  7. IP címek kinyerése
  8. Kilépés

Használjon egyszerû objektum-létrehozást (new kulcsszó) a szolgáltatás példányosításához.

## 7. Egységtesztek készítése

**Helye:** `LogAnalyzer.Tests` projekt

Hozzon létre legalább 6 tesztesetet xUnit keretrendszerrel:

### 7.1 LogAnalyzerServiceTests osztály
- `ReadLogFile_ValidFile_ReturnsCorrectEntries()` - Érvényes fájl beolvasásának tesztelése
- `IsValidLogFormat_ValidFormat_ReturnsTrue()` - Formátum validálás tesztelése érvényes sorral
- `IsValidLogFormat_InvalidFormat_ReturnsFalse()` - Formátum validálás tesztelése érvénytelen sorral
- `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()` - Hibák számolásának tesztelése
- `ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()` - E-mail kinyerés tesztelése
- `ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()` - IP cím kinyerés tesztelése

Használjon test data setup-ot és Assert metódusokat az eredmények ellenõrzésére.

## 8. Mintafájl és dokumentáció

**Helye:** Megoldás gyökér mappája

### 8.1 Minta naplófájl
Hozzon létre egy `sample.log` fájlt legalább 20 sorral, amely tartalmaz:
- Különbözõ naplószinteket (INFO, WARNING, ERROR, DEBUG)
- Különbözõ felhasználókat
- E-mail címeket a naplóüzenetekben
- IP címeket a naplóüzenetekben
- Néhány hibás formátumú sort is a teszteléshez

Példa sorok:
```
[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity detected from 10.0.0.5
[2024-01-15 10:33:05] [DEBUG] [system] Email sent to support@company.hu successfully
```

### 8.2 README.md
Készítsen dokumentációt, amely tartalmazza:
- A projekt leírását
- Futtatási utasításokat
- A naplófájl formátumának leírását
- A reguláris kifejezések alkalmazásának magyarázatát
- Példákat a használatra

## Értékelési szempontok

- **Kód minõség:** Clean code elvek betartása, megfelelõ névadás
- **LINQ használat:** Hatékony és olvasható LINQ lekérdezések
- **Reguláris kifejezések:** Helyes regex minták létrehozása és alkalmazása
- **Tesztelés:** Átfogó tesztlefedettség, jól strukturált tesztek
- **Hibakezelés:** Megfelelõ exception handling
- **Projekt struktúra:** Tiszta kód szervezés, megfelelõ felelõsség megosztás
- **Felhasználói élmény:** Intuitív konzol interfész

## Határidõ és leadás

A feladatot a vizsga idõkeretén belül kell elkészíteni. A megoldásnak mind a három projektben futtathatónak és teszteltnek kell lennie.

