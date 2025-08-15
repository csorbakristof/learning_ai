# Vizsgafeladat az EViP kurzushoz

Ez a megold�s egy vizsgafeladat mintamegval�s�t�sa, amely napl�f�jlok elemz�s�vel foglalkozik.
A vizsga alapvet� C# szintaxisra, IEnumerable, LINQ, regul�ris kifejez�sek �s xUnit tesztel�sre f�kusz�l.
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
- `string Timestamp` - A napl�bejegyz�s id�pontja sz�veg form�tumban
- `string Level` - A napl� szintje (INFO, WARNING, ERROR, DEBUG)
- `string Message` - A napl��zenet
- `string User` - A felhaszn�l� neve (opcion�lis)

### 2.2 LogAnalyzerService oszt�ly
Hozza l�tre a `LogAnalyzerService` oszt�lyt a k�vetkez� met�dusokkal:
- `List<LogEntry> ReadLogFile(string filePath)`
- `IEnumerable<LogEntry> FilterByLevel(IEnumerable<LogEntry> entries, string level)`
- `int CountErrorEntries(IEnumerable<LogEntry> entries)`
- `Dictionary<string, int> GetUserActivitySummary(IEnumerable<LogEntry> entries)`
- `bool IsValidLogFormat(string logLine)`
- `List<string> ExtractEmailAddresses(IEnumerable<LogEntry> entries)`
- `List<string> ExtractIPAddresses(IEnumerable<LogEntry> entries)`

## 3. Napl�f�jl beolvas�sa �s form�tum valid�l�sa

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` oszt�ly

### 3.1 F�jl beolvas�sa
Implement�lja a `ReadLogFile` met�dust, amely:
- Beolvassa a napl�f�jlt soronk�nt
- Minden sort feldolgoz �s l�trehozza a `LogEntry` objektumokat
- K�pes kezelni a k�vetkez� form�tumot: `[YYYY-MM-DD HH:mm:ss] [LEVEL] [USER] Message`
- P�ld�ul: `[2024-01-15 10:30:45] [ERROR] [john.doe] Database connection failed`
- Hibakezel�st tartalmaz nem l�tez� f�jl eset�n

### 3.2 Form�tum valid�l�s regul�ris kifejez�ssel
Implement�lja az `IsValidLogFormat` met�dust, amely:
- Regul�ris kifejez�st haszn�l a napl�sor form�tum�nak ellen�rz�s�re
- Ellen�rizze, hogy a sor a v�rt form�tumban van-e: sz�gletes z�r�jelekben d�tum �s id�, majd sz�gletes z�r�jelekben a napl� szint, majd sz�gletes z�r�jelekben a felhaszn�l�n�v, v�g�l az �zenet
- **Tipp:** Gondoljon a sz�gletes z�r�jelekre, sz�mjegyekre, k�t�jelekre, kett�spontokra �s a n�gy lehets�ges napl� szintre
- Visszaadja, hogy a sor megfelel-e a v�rt form�tumnak

## 4. Napl�bejegyz�sek sz�r�se �s elemz�se

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` oszt�ly

### 4.1 Szint alap� sz�r�s
Implement�lja a `FilterByLevel` met�dust, amely:
- LINQ Where() met�dussal sz�ri az adott szint� bejegyz�seket
- Case-insensitive �sszehasonl�t�st haszn�l

### 4.2 Hib�k sz�mol�sa
Implement�lja a `CountErrorEntries` met�dust, amely:
- LINQ Count() met�dussal sz�molja meg az ERROR szint� bejegyz�seket
- Case-insensitive �sszehasonl�t�st haszn�l

### 4.3 Felhaszn�l�i aktivit�s elemz�se
Implement�lja a `GetUserActivitySummary` met�dust, amely:
- LINQ GroupBy �s ToDictionary haszn�lat�val csoportos�tja a bejegyz�seket felhaszn�l�k szerint
- Visszaadja, hogy melyik felhaszn�l� h�ny bejegyz�st hozott l�tre

## 5. Regul�ris kifejez�sek alkalmaz�sa adatkinyer�shez

**Helye:** `LogAnalyzer.Core` projekt, `LogAnalyzerService` oszt�ly

### 5.1 E-mail c�mek kinyer�se
Implement�lja az `ExtractEmailAddresses` met�dust, amely:
- Regul�ris kifejez�st haszn�l e-mail c�mek megtal�l�s�hoz a napl��zenetekben
- **P�lda e-mail c�mek a napl�ban:** `john.doe@company.com`, `support@website.hu`, `admin_user@test-site.org`
- **Tipp:** Az e-mail c�m �ltal�ban bet�kb�l, sz�mokb�l �s bizonyos speci�lis karakterekb�l �ll, majd egy @ jel, majd �jra bet�k/sz�mok, egy pont, �s v�g�l a domain v�gz�d�s
- LINQ SelectMany �s Distinct haszn�lat�val adja vissza az egyedi e-mail c�meket

### 5.2 IP c�mek kinyer�se
Implement�lja az `ExtractIPAddresses` met�dust, amely:
- Regul�ris kifejez�st haszn�l IPv4 c�mek megtal�l�s�hoz a napl��zenetekben
- **P�lda IP c�mek a napl�ban:** `192.168.1.100`, `10.0.0.5`, `172.16.254.1`
- **Tipp:** IPv4 c�m 4 db 0-255 k�z�tti sz�mb�l �ll, pontokkal elv�lasztva. Gondoljon arra, hogy egy-egy sz�m 1-3 jegy� lehet
- LINQ SelectMany �s Distinct haszn�lat�val adja vissza az egyedi IP c�meket

## 6. Konzol alkalmaz�s k�sz�t�se

**Helye:** `LogAnalyzer.Console` projekt, `Program.cs`

K�sz�tsen egy interakt�v konzol alkalmaz�st, amely:
- Men� alap� navig�ci�t biztos�t
- L�trehoz egy `LogAnalyzerService` p�ld�nyt a Main met�dusban
- A k�vetkez� funkci�kat k�n�lja:
  1. Napl�f�jl bet�lt�se
  2. �sszes bejegyz�s megjelen�t�se
  3. Adott szint� bejegyz�sek sz�r�se
  4. Hib�k sz�m�nak megjelen�t�se
  5. Felhaszn�l�i aktivit�s �sszes�t�
  6. E-mail c�mek kinyer�se
  7. IP c�mek kinyer�se
  8. Kil�p�s

Haszn�ljon egyszer� objektum-l�trehoz�st (new kulcssz�) a szolg�ltat�s p�ld�nyos�t�s�hoz.

## 7. Egys�gtesztek k�sz�t�se

**Helye:** `LogAnalyzer.Tests` projekt

Hozzon l�tre legal�bb 6 tesztesetet xUnit keretrendszerrel:

### 7.1 LogAnalyzerServiceTests oszt�ly
- `ReadLogFile_ValidFile_ReturnsCorrectEntries()` - �rv�nyes f�jl beolvas�s�nak tesztel�se
- `IsValidLogFormat_ValidFormat_ReturnsTrue()` - Form�tum valid�l�s tesztel�se �rv�nyes sorral
- `IsValidLogFormat_InvalidFormat_ReturnsFalse()` - Form�tum valid�l�s tesztel�se �rv�nytelen sorral
- `CountErrorEntries_WithErrorEntries_ReturnsCorrectCount()` - Hib�k sz�mol�s�nak tesztel�se
- `ExtractEmailAddresses_WithEmails_ReturnsCorrectEmails()` - E-mail kinyer�s tesztel�se
- `ExtractIPAddresses_WithIPs_ReturnsCorrectIPs()` - IP c�m kinyer�s tesztel�se

Haszn�ljon test data setup-ot �s Assert met�dusokat az eredm�nyek ellen�rz�s�re.

## 8. Mintaf�jl �s dokument�ci�

**Helye:** Megold�s gy�k�r mapp�ja

### 8.1 Minta napl�f�jl
Hozzon l�tre egy `sample.log` f�jlt legal�bb 20 sorral, amely tartalmaz:
- K�l�nb�z� napl�szinteket (INFO, WARNING, ERROR, DEBUG)
- K�l�nb�z� felhaszn�l�kat
- E-mail c�meket a napl��zenetekben
- IP c�meket a napl��zenetekben
- N�h�ny hib�s form�tum� sort is a tesztel�shez

P�lda sorok:
```
[2024-01-15 10:30:45] [ERROR] [john.doe] Failed login attempt from 192.168.1.100
[2024-01-15 10:31:20] [INFO] [jane.smith] User registered with email john.doe@company.com
[2024-01-15 10:32:10] [WARNING] [admin] Suspicious activity detected from 10.0.0.5
[2024-01-15 10:33:05] [DEBUG] [system] Email sent to support@company.hu successfully
```

### 8.2 README.md
K�sz�tsen dokument�ci�t, amely tartalmazza:
- A projekt le�r�s�t
- Futtat�si utas�t�sokat
- A napl�f�jl form�tum�nak le�r�s�t
- A regul�ris kifejez�sek alkalmaz�s�nak magyar�zat�t
- P�ld�kat a haszn�latra

## �rt�kel�si szempontok

- **K�d min�s�g:** Clean code elvek betart�sa, megfelel� n�vad�s
- **LINQ haszn�lat:** Hat�kony �s olvashat� LINQ lek�rdez�sek
- **Regul�ris kifejez�sek:** Helyes regex mint�k l�trehoz�sa �s alkalmaz�sa
- **Tesztel�s:** �tfog� tesztlefedetts�g, j�l struktur�lt tesztek
- **Hibakezel�s:** Megfelel� exception handling
- **Projekt strukt�ra:** Tiszta k�d szervez�s, megfelel� felel�ss�g megoszt�s
- **Felhaszn�l�i �lm�ny:** Intuit�v konzol interf�sz

## Hat�rid� �s lead�s

A feladatot a vizsga id�keret�n bel�l kell elk�sz�teni. A megold�snak mind a h�rom projektben futtathat�nak �s teszteltnek kell lennie.

