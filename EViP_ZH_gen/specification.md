# Vizsgafeladat az EViP kurzushoz

Ez a megold�s egy vizsgafeladat mintamegval�s�t�sa, amely napl�f�jlok elemz�s�vel foglalkozik.
A vizsga alapvet� C# szintaxisra, IEnumerable, LINQ, �s xUnit tesztel�sre f�kusz�l.
A hallgat�knak a megold�st a null�r�l kell elk�sz�teni�k. A megold�snak 3 projektet kell tartalmaznia: egy oszt�lyk�nyvt�rat, egy konzol alkalmaz�st �s egy teszt projektet. Mind a konzol alkalmaz�s, mind a teszt projekt hivatkozni fog az oszt�lyk�nyvt�rra.

# Konkr�t vizsgafeladat: Napl�f�jlok elemz�se

A feladat c�lja, hogy a hallgat�k egy napl�f�jlokat elemz� rendszert k�sz�tsenek, amely a k�vetkez� r�szfeladatokat tartalmazza:

## 1. Projekt strukt�ra l�trehoz�sa

**Helye:** Megold�s gy�k�r mapp�ja

Hozza l�tre a k�vetkez� projekt strukt�r�t:
- `LogAnalyzer.Core` - Class Library (.NET 8) projekt az �zleti logik�hoz
- `LogAnalyzer.Console` - Console Application (.NET 8) projekt a felhaszn�l�i fel�lethez
- `LogAnalyzer.Tests` - Class Library (.NET 8) projekt a tesztekhez (xUnit referenci�val)

�ll�tsa be a projekt referenci�kat:
- `LogAnalyzer.Console` hivatkozzon a `LogAnalyzer.Core` projektre
- `LogAnalyzer.Tests` hivatkozzon a `LogAnalyzer.Core` projektre

## 2. Napl�bejegyz�s modell �s szolg�ltat�s l�trehoz�sa

**Helye:** `LogAnalyzer.Core` projekt

Hozza l�tre a k�vetkez� oszt�lyokat:

### 2.1 LogEntry modell
K�sz�tsen egy `LogEntry` oszt�lyt a k�vetkez� tulajdons�gokkal:
- `DateTime Timestamp` - A napl�bejegyz�s id�pontja
- `string Level` - A napl� szintje (INFO, WARNING, ERROR, DEBUG)
- `string Message` - A napl��zenet
- `string User` - A felhaszn�l� neve (opcion�lis)

### 2.2 ILogAnalyzerService interf�sz
Defini�ljon egy interf�szt a k�vetkez� met�dusokkal:
- `Task<List<LogEntry>> ReadLogFileAsync(string filePath)`
- `IEnumerable<LogEntry> FilterByDate(IEnumerable<LogEntry> entries, DateTime date)`
- `int CountErrorEntries(IEnumerable<LogEntry> entries)`
- `Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)`
- `IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)`

### 2.3 LogAnalyzerService implement�ci�
Implement�lja az `ILogAnalyzerService` interf�szt LINQ haszn�lat�val.

## 3. Napl�f�jl beolvas�sa �s feldolgoz�sa

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` oszt�ly

Implement�lja a `ReadLogFileAsync` met�dust, amely:
- Aszinkron m�don olvassa be a napl�f�jlt
- Feldolgozza a sorokat �s l�trehozza a `LogEntry` objektumokat
- K�pes kezelni a k�vetkez� form�tumot: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message`
- P�ld�ul: `[2024-01-15 10:30:45] [ERROR] [john.doe] Database connection failed`
- Hibakezel�st tartalmaz �rv�nytelen sorok eset�n

## 4. Napl�bejegyz�sek sz�r�se �s elemz�se

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` oszt�ly

### 4.1 D�tum alap� sz�r�s
Implement�lja a `FilterByDate` met�dust LINQ haszn�lat�val, amely:
- Egy adott naphoz tartoz� bejegyz�seket adja vissza
- Csak a d�tumot veszi figyelembe, az id�t nem

### 4.2 Hib�k sz�mol�sa
Implement�lja a `CountErrorEntries` met�dust, amely:
- LINQ Count() met�dussal sz�molja meg az ERROR szint� bejegyz�seket
- Case-insensitive �sszehasonl�t�st haszn�l

### 4.3 Felhaszn�l�i aktivit�s elemz�se
Implement�lja a `GetUserActivitySummary` met�dust, amely:
- LINQ GroupBy �s ToDictionary haszn�lat�val csoportos�tja a bejegyz�seket felhaszn�l�k szerint
- Visszaadja, hogy melyik felhaszn�l� h�ny bejegyz�st hozott l�tre

### 4.4 Szint alap� sz�r�s
Implement�lja a `FilterByLevel` met�dust, amely:
- Egy adott napl�szinthez tartoz� bejegyz�seket sz�ri ki
- Case-insensitive �sszehasonl�t�st haszn�l

## 5. Konzol alkalmaz�s k�sz�t�se

**Helye:** `LogAnalyzer.Console` projekt, `Program.cs`

K�sz�tsen egy interakt�v konzol alkalmaz�st, amely:
- Men� alap� navig�ci�t biztos�t
- Lehet�s�get ad napl�f�jl megad�s�ra
- A k�vetkez� funkci�kat k�n�lja:
  1. Napl�f�jl bet�lt�se
  2. �sszes bejegyz�s megjelen�t�se
  3. Adott d�tumhoz tartoz� bejegyz�sek sz�r�se
  4. Hib�k sz�m�nak megjelen�t�se
  5. Felhaszn�l�i aktivit�s �sszes�t�
  6. Adott szint� bejegyz�sek sz�r�se
  7. Kil�p�s

Haszn�ljon dependency injection-t az `ILogAnalyzerService` injekt�l�s�hoz.

## 6. Egys�gtesztek k�sz�t�se

**Helye:** `LogAnalyzer.Tests` projekt

Hozzon l�tre legal�bb 5 tesztesetet xUnit keretrendszerrel:

### 6.1 LogAnalyzerServiceTests oszt�ly
- `ReadLogFileAsync_ValidFile_ReturnsCorrectEntries()` - �rv�nyes f�jl beolvas�s�nak tesztel�se
- `FilterByDate_ValidDate_ReturnsFilteredEntries()` - D�tum alap� sz�r�s tesztel�se
- `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()` - Hib�k sz�mol�s�nak tesztel�se
- `GetUserActivitySummary_WithMultipleUsers_ReturnsCorrectSummary()` - Felhaszn�l�i aktivit�s tesztel�se
- `FilterByLevel_ValidLevel_ReturnsFilteredEntries()` - Szint alap� sz�r�s tesztel�se

Haszn�ljon test data setup-ot �s Assert met�dusokat az eredm�nyek ellen�rz�s�re.

## 7. Mintaf�jl �s dokument�ci�

**Helye:** Megold�s gy�k�r mapp�ja

### 7.1 Minta napl�f�jl
Hozzon l�tre egy `sample.log` f�jlt legal�bb 20 sorral, k�l�nb�z�:
- D�tumokkal
- Napl�szintekkel (INFO, WARNING, ERROR, DEBUG)
- Felhaszn�l�kkal
- �zenetekkel

### 7.2 README.md
K�sz�tsen dokument�ci�t, amely tartalmazza:
- A projekt le�r�s�t
- Futtat�si utas�t�sokat
- A napl�f�jl form�tum�nak le�r�s�t
- P�ld�kat a haszn�latra

## �rt�kel�si szempontok

- **K�d min�s�g:** Clean code elvek betart�sa, megfelel� n�vad�s
- **LINQ haszn�lat:** Hat�kony �s olvashat� LINQ lek�rdez�sek
- **Aszinkron programoz�s:** Task �s async/await helyes haszn�lata
- **Tesztel�s:** �tfog� tesztlefedetts�g, j�l struktur�lt tesztek
- **Hibakezel�s:** Megfelel� exception handling
- **Projekt strukt�ra:** Tiszta architekt�ra, megfelel� separation of concerns
- **Felhaszn�l�i �lm�ny:** Intuit�v konzol interf�sz

## Hat�rid� �s lead�s

A feladatot a vizsga id�keret�n bel�l kell elk�sz�teni. A megold�snak mind a h�rom projektben futtathat�nak �s teszteltnek kell lennie.

