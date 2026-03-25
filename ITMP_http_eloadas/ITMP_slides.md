# Dia 1: Címlap

### Címsor

Nagy Nyelvi Modellek (LLM-ek) Használata a Middle School Oktatásban

### Szöveges tartalom

**Práktól a kollaborációig**

Prompt minták és AI asszisztált tanulás

### Illusztráció promptja

Modern, minimalista illusztráció egy diákról, aki egy futurisztikus holografikus képernyő előtt ül, ami AIChat interfészt mutat. Meleg, barátságos színek (kék, zöld árnyalatok), oktatási környezet, inspiráló és optimista hangulat. Flat design stílus, egyszerű vonalak.

### Megjegyzések az előadónak

Bevezető dia. Hangsúlyozd, hogy nem az AI helyettesíti a gondolkodást, hanem eszköz a tanuláshoz. A cél: megtanítani a diákokat hatékonyan kommunikálni az AI-val és kritikusan értékelni a válaszokat.

# Dia 2: Miért fontos?

### Címsor

Az AI-val való kommunikáció mint új kompetencia

### Szöveges tartalom

**A kérdezéstől az együttműködésig**

• Gyakorlati készségfejlesztés
• Promptolási minták elsajátítása  
• Kritikus gondolkodás erősítése
• Interdiszciplináris alkalmazások

**Ma már nem elég jó kérdést feltenni - meg kell tanulni együttműködni az AI-val.**

### Illusztráció promptja

Infografika stílusú kép: bal oldalon "Régen" felirattal egy egyszerű kérdőjel, jobb oldalon "Ma" felirattal összetett párbeszéd buborékok hálózata. Középen át egy nyíl, ami az evolúciót mutatja. Modern, tiszta dizájn, professzionális oktatási stílus.

### Megjegyzések az előadónak

Hangsúlyozd a paradigmaváltást: nem csupán válaszokat kérünk, hanem iteratív folyamatban dolgozunk az AI-val. Ez új készség, amit tanítani kell, mint a számítógép-használatot annak idején.

# Dia 3: Standard komponensek

### Címsor

A Jó Prompt Építőkövei: Kontextus-Feladat-Korlátozás

### Szöveges tartalom

**5 alapvető elem:**

1. **Perszona** - Ki legyen az AI? (pl. "Te egy történelemtanár vagy")
2. **Feladat** - Mit csináljon? (Egyértelmű, cselekvő ige)
3. **Kontextus** - Miért és kinek? (Háttér, célközönség)
4. **Korlátozások** - Milyen határok? (Hossz, hangnem, tiltott témák)
5. **Formátum** - Milyen formában? (Táblázat, lista, JSON)

### Illusztráció promptja

Öt színes építőkocka piramis formában egymásra helyezve, mindegyiken egy-egy ikon: korona (Perszona), cselekvés nyíl (Feladat), kontextus puzzle (Kontextus), kerítés (Korlátozások), sablon (Formátum). Világos, oktatási infografika stílus.

### Megjegyzések az előadónak

Ez a dia a legfontosabb! Mutass konkrét példát: "Te egy biológiatanár vagy (PERSZONA). Magyarázd el a fotoszintézist (FELADAT) 12 éves diákoknak (KONTEXTUS) maximum 100 szóban (KORLÁTOZÁS) 3 pontban (FORMÁTUM)." Hasonlítsd össze egy gyenge prompttal: "Mi a fotoszintézis?"

# Dia 4: Promptolási szintek

### Címsor

A "Zero-Shot-tól a Chain-of-Thought-ig" Skála

### Szöveges tartalom

**5 szint az egyszerűtől az összezettig:**

**Szint 1:** Standard Promptolás  
_Egyszerű kérdés vagy utasítás_

**Szint 2:** Few-Shot Promptolás  
_2-3 példa a kérés előtt_

**Szint 3:** Chain-of-Thought (CoT)  
_"Gondolkodj lépésről lépésre"_

**Szint 4:** Iteratív Finomítás  
_AI kritizálja saját válaszát_

**Szint 5:** Meta-Promptolás  
_AI írja meg a legjobb promptot_

### Illusztráció promptja

Lépcsőzetes diagram, öt fokozattal, minden fokozaton egy ikon: 1) egyszerű kérdőjel, 2) három példa kártya, 3) agyi hálózat gondolkodás közben, 4) körkörös nyilak (iteráció), 5) meta-szintű spirál. Felfelé mutató trend nyíl a komplexitás növekedését mutatja. Oktatási színek.

### Megjegyzések az előadónak

Fontos megjegyezni, hogy nem minden esetben kell a legmagasabb szintet használni. Az 1-es szint tökéletes egyszerű kérdésekre. A magasabb szintek akkor kellenek, amikor összetett problémát oldunk meg vagy minőségi kimenetet várunk.

# Dia 5: Szint 1-2 példák

### Címsor

Kezdő Szintek: Standard és Few-Shot

### Szöveges tartalom

**Szint 1 - Standard Promptolás:**
> "Sorold fel a Naprendszer bolygóit."

**Szint 2 - Few-Shot Promptolás:**
> "Klasszifikálj állatokat:  
> Példa 1: Delfin → Emlős → Vízi  
> Példa 2: Sas → Madár → Szárnyas  
> Most te: Cápa → ?"

**Eredmény:** A példák után pontosabb és konzisztensebb válaszok!

### Illusztráció promptja

Split-screen kép: bal oldalon egyszerű kérdés-válasz buborék, jobb oldalon három példa kártya plusz egy új kérdés. A jobb oldal kimenete részletesebb és strukturáltabb. Összehasonlító diagram stílus, világos vizuális különbség.

### Megjegyzések az előadónak

A Few-Shot technika különösen hatékony formázott kimenetekhez. Példa diákoknak: ha táblázatot akarsz, adj meg 2-3 sor példát, és az AI folytatja a mintát. Gyakorlati tipp: mindig ugyanazt a formátumot használd a példákban!

# Dia 6: Chain of Thought

### Címsor

Szint 3: "Gondolkodj lépésről lépésre"

### Szöveges tartalom

**Mikor használjuk?**
• Matematikai problémák
• Logikai fejtörők  
• Többlépéses fizikai példák

**Példa fizikára:**
_"Egy autó 0-ról 100 km/h-ra gyorsul 8 mp alatt. Old meg **lépésről lépésre**: 1) Írd fel a képleteket 2) Alakítsd át az egységeket 3) Számold ki 4) Ellenőrizd"_

**Eredmény:** Kevesebb hiba, átlátható érvelés!

### Illusztráció promptja

Vizuális folyamatábra: egy komplex matematikai probléma felülről lefelé kibontakozik lépésekre. Minden lépés egy külön dobozban, nyilak kötik össze őket. Az utolsó doboz egy pipa jellel jelzi a helyes megoldást. Tiszta, oktatási diagram stílus.

### Megjegyzések az előadónak

A CoT drámaian javítja a matematikai és logikai feladatok megoldását. Tanulmányok szerint 30-50%-kal csökken a hibaarány. Fontos: a "lépésről lépésre" kifejezés használata - ez trigger phrase az LLM számára, ami aktiválja a lassabb, gondolkodó módot.

# Dia 7: Iteratív finomítás

### Címsor

Szint 4-5: Önreflexió és Meta-Promptolás

### Szöveges tartalom

**Szint 4 - Iteratív Finomítás:**
> "Írtál egy fogalmazást. Most kritizáld: mi a gyenge benne? Javítsd!"

**Szint 5 - Meta-Promptolás:**
> "Milyen promptot kellene írnom, hogy a legjobb esszét kapjam a klímaváltozásról 500 szóban?"

**Plusz extra:** AI értékelje a promptod 1-10 skálán és adjon javítási tippeket!

### Illusztráció promptja

Két vizuális elem: 1) Körkörös nyíl szimbólum (iteráció), egy szöveg többször finomodik. 2) Meta-szint: egy prompt EGY MÁSIK promptot generál. Rekurzív, spirál jellegű ábrázolás. Modern, absztrakt oktatási stílus.

### Megjegyzések az előadónak

Ez már haladó technika, de nagyon erős eredményeket ad. Az iteratív finomítás megmutatja a diákoknak, hogy az AI nem "egylövetű" eszköz - párbeszédet folytatunk vele. A meta-prompting esetén az AI becomes "prompt coach" - ez különösen hasznos, amikor nem tudják a diákok, hogyan kezdjenek hozzá.

# Dia 8: Prompt minták I

### Címsor

Promptolási Minták Áttekintése (1/2)

### Szöveges tartalom

**Perszona minta:**  
_"Ki vagy?" → Hangnem, stílus, szakmai zsargon_

**Few-Shot minta:**  
_"Kövesd a példám" → Adatformázás, osztályozás_

**Chain of Thought:**  
_"Lassíts és gondolkodj" → Logika, matematika_

**Mikor melyiket?**
• Perszona → Stílus kell
• Few-Shot → Formátum kell  
• CoT → Érvelés kell

### Illusztráció promptja

Három kártya egy táblán, mindegyiken egy minta neve és egy egyszerű ikon. Perszona: színészi maszk, Few-Shot: három példa kártya, Chain of Thought: agyi hálózat. Alattuk nyilak mutatják a használati eseteket. Card-based infographic design.

### Megjegyzések az előadónak

Hangsúlyozd: nincs "legjobb" minta, minden feladatnak megvan a megfelelő eszköze. Egy jó analógia: mint a szerszámok - kalapáccsal verhetsz szeget, de csavarhoz csavarhúzó kell. A diákoknak meg kell tanulniuk felismerni, melyik feladathoz melyik minta passzol.

# Dia 9: Prompt minták II

### Címsor

Promptolási Minták Áttekintése (2/2)

### Szöveges tartalom

**Korlátozás/Negatív minta:**  
_"Maradj a határokon belül" → Szigorú követelmények_

**Példa:** "Foglald össze Petőfit 50 szóban, a 'forradalom' szó nélkül"

**Chain of Density minta:**  
_"Jobbat, ne többet" → Információsűrűség növelése_

**Példa:** "Írd át ezt 150 szóból 100-ba, de több ténnyel!"

### Illusztráció promptja

Két vizuális elem: 1) Kerítés szimbólum "ne menj túl" táblával (Korlátozás), 2) Tömörítés folyamat - nagy szövegblokk összenyomódik kisebbre, de több adatot tartalmaz (sűrűség nyilak). Infographic stílus, világos, oktatási.

### Megjegyzések az előadónak

A korlátozások fontosak valós helyzetekben: karakterlimit, tiltott kifejezések, etc. A Chain of Density újságírói technika - fordított összefoglaló: egyre rövidebb, de egyre több információval. Gyakorlati példa: social media posztok írásakor hasznos.

# Dia 10: Használati ellenőrzőlista

### Címsor

Bölcs AI Használat Diákoknak

### Szöveges tartalom

**4 alapelv minden használat előtt:**

✓ **Szerepjáték** - Rendelj perszonát a kontextushoz  
✓ **Tényfelderítés** - Ellenőrizz legalább 1 állítást külső forrással  
✓ **Etikai ellenőrzés** - Van-e elfogultság a válaszban?  
✓ **Hivatkozás** - Jelöld az AI-generált részeket!

**Ne feledd:** Az AI eszköz, nem helyettesítő. Te vagy a felelős!

### Illusztráció promptja

Checklist ikon négy pipával, mindegyik mellett egy kis ikon: színészi maszk, nagyító, mérleg (etika), idézőjel (hivatkozás). A kép alja egy figyelmeztető sáv: "Te vagy a kapitány, az AI a navigátor." Modern, clean checklist design.

### Megjegyzések az előadónak

Ez kritikus dia! Hangsúlyozd az etikai szempontokat. Az AI hallucinálhat, elfogult lehet, és soha ne másold be ellenőrzés nélkül. Analógia: mint a számológép matekban - használhatod, de értened kell mit csinál. A hivatkozás különösen fontos akadémiai integritás szempontjából.

# Dia 11: Gyakorlati tippek

### Címsor

Hogyan Kezdd? - Gyakorlati Tippek

### Szöveges tartalom

**1. Kezd egyszerűen** → Standard prompt, aztán finomítsd

**2. Használj példákat** → Few-Shot mindig segít

**3. Kérj lépéseket** → CoT összetett problémáknál

**4. Iterálj** → Első válasz ritkán tökéletes

**5. Értékeltess** → "Pontozd 1-10-ig és javíts!"

**Emlékeztető:** Gyorsabban tanulsz, ha hibázol és javítasz!

### Illusztráció promptja

Öt lépcsőfok felfelé, minden fokozaton egy egyszerű ikon és szám. Alul egy "START" tábla, felül egy "MESTER" csillag. Az egész egy útmutató jellegű vizualizáció - "learning journey" stílus. Inspiráló, motiváló színek.

### Megjegyzések az előadónak

Gyakorlati tanács: kezdjék egy egyszerű kérdéssel, és ha nem tetszik a válasz, ne dobjátok el! Kérdezzétek: "Miért ez a válasz?" vagy "Tudnál másképp is válaszolni?" Ez megtanítja őket az iteratív munkára. Hangsúlyozd: a hibázás normális és hasznos része a tanulásnak.

# Dia 12: Összegzés

### Címsor

Összefoglalás: AI mint Tanulási Partner

### Szöveges tartalom

**Mit tanultunk?**

• **5 prompt komponens** - építőkövek
• **5 promptolási szint** - egyszerűtől összetettig
• **5 hasznos minta** - eszköztár minden helyzetre
• **4 etikai elv** - felelős használat

**Következő lépés:** Próbáljátok ki! Kísérletezzetek!

**Remember:** A jó promptolás gyakorlat kérdése.

### Illusztráció promptja

Központi elem: mosolygós diák laptop előtt, körülötte keringő ikonok az összes tanult elemmel (perszona, Few-Shot, CoT, checklist, stb). Dinamikus, optimista kompozíció, ami azt sugallja: "készen állsz elkezdeni!" Inspiráló, záró slide stílus, vibráns színek.

### Megjegyzések az előadónak

Záró dia - optimista hangvétel! Hangsúlyozd: ez csak a kezdet, a készségfejlesztés folyamatos. Adj gyakorlati házi feladatot: mindenki írjon egy jó promptot egy választott témára az 5 komponens használatával. Következő órán megbeszélitek. Bátorítsd őket a kísérletezésre!

