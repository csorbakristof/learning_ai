# Feladat 1: Történelmi Interjú

### Címsor

Történelmi Interjú Feladat - Beszélgess a múlttal (Történelem)

### Feladat leírása

**A feladat:** Promptold az LLM-et, hogy egy konkrét történelmi személyként viselkedjen (pl. Széchenyi István vagy Kossuth Lajos).

**Informatikai fókusz:** Iteratív Promptolás - A diákoknak finomítaniuk kell a "rendszer promptot" hogy tartalmazzon specifikus korlátozásokat, mint például 19. századi szókincs vagy utalások konkrét reformokra, események a szabadságharcból.

**Kritikus gondolkodás:** Hasonlítsd össze az AI válaszokat tankönyvekkel, hogy azonosítsd a hallucinációkat.

### Tanulság, mire jó

• **Történelmi empátia** - A diákok egy történelmi személy szemszögéből gondolkodnak
• **Kontextus fontossága** - Megtanulják, hogy az időbeli és kulturális kontextus hogyan befolyásolja a válaszokat
• **Hallucinációfelismerés** - Gyakorolják a tényfelderítést és forrásösszehasonlítást
• **Prompt finomítás** - Iteratív módon javítják a promptot, hogy hiteles választ kapjanak

### Megjegyzés az előadónak

Ez a feladat kiválóan demonstrálja a perszona és kontextus fontosságát. Hangsúlyozd: minél specifikusabb a történelmi keret (dátum, helyzet, esemény), annál hitelesebb a válasz. Fontos megemlíteni, hogy az AI nem "tudja" a történelmet - mintákat reprodukál a tanítóadatokból. Ezért KRITIKUS a tankönyvi ellenőrzés. Jó példa arra is, hogyan lehet az AI-t oktatási eszközként használni szerepjátékhoz, de mindig kritikus forrásértékeléssel együtt. Tipp: kérd meg a diákokat, hogy kezdjék egyszerű prompttal, majd iteratívan adjanak hozzá korlátozásokat (időszak, nyelvezet, tiltott kifejezések).

### Példa prompt 1

"Te Széchenyi István gróf vagy, 1830-ban járunk, Pozsonyban, a magyar országgyűlés idején. Beszélj első személyben a reformelképzeléseidről: a lóverseny megalapításáról, a Lánchíd tervéről, és hogy miért szükséges a nemzeti fejlődéshez a modernizáció. Használj korabeli kifejezéseket és a 19. századi magyar nemesség udvarias, mégis reformer stílusát. Ne említs semmit, ami 1830 után történt. Kezdd a választ így: 'Méltóztassék meghallgatni elképzeléseimet...'"

### Példa prompt 2

"Te Kossuth Lajos vagy, 1848. április 11-én, éppen visszatértél a pozsonyi országgyűlésből Pestre. Szerepedben válaszolj kérdésekre a függetlenségi törekvésekről, a jobbágyfelszabadítás jelentőségéről és a nemzetőrség felállításának sürgősségéről. Használj szenvedélyes, retorikus, korabeli magyaros nyelvet és tükrözd a kor nemzeti lelkesedését. Utalj konkrét törvénycikkekre és a márciusi ifjak mozgalmára."

# Feladat 2: Algoritmikus Költő

### Címsor

Algoritmikus Költő Feladat - Amikor az AI verset ír (Irodalom)

### Feladat leírása

**A feladat:** Generálj egy verset egy meghatározott stílusban (pl. Petőfi vagy Arany János stílusában) egy modern technikai témáról, mint a kiberbiztonság vagy a mesterséges intelligencia.

**Informatikai fókusz:** Mintafelismerés - Elemezd, hogyan változtatja meg a kimenetet a stílusbeli kulcsszavak vagy a "hőmérséklet" beállítások módosítása.

### Tanulság, mire jó

• **Stílusimitáció** - Megérteni, hogy az AI hogyan reprodukál költői stílusokat
• **Kreatív prompt tervezés** - Konkrét stílusjegyek, formák és témák meghatározása
• **Anachronizmus felismerése** - Modern fogalmak régi stílusban való megfogalmazása
• **Irodalmi elemzés** - Összehasonlítani az eredeti költő stílusát az AI által generált verssel

### Megjegyzés az előadónak

Ez a feladat kiválóan mutatja a kreatív AI használat lehetőségeit ÉS korlátait. Az AI nem "ért" költészetet - statisztikai mintákat követ. Ezért fontos megbeszélni: mi az ami "petőfis" egy versben? (népi képek, egyszerű nyelv, direkt megszólítás, hazafias témák). A diákok tanulják meg a stílusjegyeket explicit módon megfogalmazni a promptban. Érdekes kísérlet: ugyanazt a verset generáltatni különböző hőmérséklet beállításokkal (ha a használt eszköz támogatja) - alacsony érték = kiszámítható, magas = kreatív/random. Ez jó alkalom beszélni az AI kreativitásáról: valóban kreatív, vagy csak rekombinálja a meglévő mintákat?

### Példa prompt 1

"Írj egy verset Petőfi Sándor jellegzetes stílusában a mesterséges intelligenciáról. 

Stílusjegyek (kötelezően alkalmazandók):
- Népi költészeti elemek: egyszerű, közérthető nyelvezet
- Rövid sorok (8-10 szótagos jambikus vagy trochaikus ritmus)
- Erős, vizuális képek (természeti vagy hétköznapi metaforák)
- Direkt megszólítás: közvetlenül szólj az olvasóhoz/AI-hoz
- Hazafias vagy szabadság-téma átültetése technológiai kontextusba
- Lírai én erőteljes jelenléte

Forma:
- Hossz: 16 sor (4 versszak x 4 sor)
- Rímséma: keresztrím (ABAB)
- Ütemhangsúlyos magyar verselés

Tartalom:
- Téma: AI és emberi szabadság, vagy AI mint új kor hajnala
- Használj modern fogalmakat (algoritmus, adatok, gépek), de népies stílusban
- Optimista vagy forradalmi hangvétel
- Érzelmi hangsúly: lelkesedés vagy aggodalom

Példa indítás: 'Mit bánom én...' vagy 'Egy világot láttam...' kezdéssel"

### Példa prompt 2

"Alkoss egy balladát Arany János modorában a kiberbiztonságról és az adatvédelemről.

Stílusjegyek (kötelezően alkalmazandók):
- Ballada műfaji jellemzők: epikus történetvezetés, drámai csúcspont, erkölcsi tanulság
- Régies, archaikus nyelv (pl. 'vala', 'lőn', 'tudá')
- Lassú tempó, komor, elmélkedő hangnem
- Metaforikus képek (pl. várfalak=tűzfalak, kémek=hackerek)
- Párbeszédek és belső monológok
- Tragikus vagy figyelmeztető kimenetel

Forma:
- Hossz: 20-24 sor (5-6 versszak x 4 sor)
- Rímséma: páros rím (AABB) vagy ölelkező (ABBA)
- Ritmus: Szabályos ütemhangsúlyos ritmus

Tartalom:
- Történet: egy karakter (pl. 'Az ifjú lovag' = fiatal programozó) aki nem védi adatait
- Cselekmény: Adatlopás/hackertámadás mint ballada konfliktus
- Erkölcsi tanulság: A technológia veszélyeinek felismerése, óvatosság fontossága
- Befejezés: Tragikus vagy figyelmeztető (pl. 'S azóta...' formulával)

Példa indítás: 'Vala egykor egy ifjú remek...' vagy 'A hálón túl, nagy mélyben...' stílusban"

# Feladat 3: Adat Elfogultság Detektív

### Címsor

Adat Elfogultság Detektív - Keresd a torzítást! (Társadalomismeret & Matematika)

### Feladat leírása

**A feladat:** Kérj egy listát a "10 híres tudósról" és elemezd az eredményeket demográfiai elfogultság szempontjából.

**Informatikai fókusz:** Tanítási Adat Tudatosság - A diákoknak egy "Elfogultság-mentesítő Promptot" kell tervezniük, hogy globálisan reprezentatív kimenetet biztosítsanak.

### Tanulság, mire jó

• **AI elfogultság felismerése** - Megérteni, hogy az AI tükrözi a tanítóadatok torzításait
• **Demográfiai reprezentáció** - Tudatosítani a nem, földrajzi eloszlás, korszak diverzitását
• **Prompt mérnökség** - Megtanulni explicit korlátozásokkal ellensúlyozni az elfogultságot
• **Adatvizualizáció** - Grafikusan ábrázolni az eredmények megoszlását (nem, kontinens, korszak)

### Megjegyzés az előadónak

Ez talán a LEGFONTOSABB kritikus gondolkodási feladat! Az AI-k többnyire nyugati, férfi, történelmi alakokat listáznak, mert a tanítóadatok így torzítottak. Ez NEM rosszindulat, hanem a történelmi és kulturális kontextus tükröződése. Fontos üzenet: az AI objektívnek TŰNIK, de nem az. A diákok készítsenek statisztikát: hány férfi/nő, hány európai/ázsiai/afrikai/amerikai, hány 20. század előtti/utáni. Aztán tervezzenek "debiasing" promptot explicit kvótákkal. Beszéljétek meg: ez kompenzáció vagy pozitív diszkrimináció? Nincs egyértelmű válasz - ez etikai kérdés. A lényeg: lássák, hogy a promptolás tud befolyásolni, és felelősség kérdése.

### Példa prompt 1

"Sorolj fel 10 híres tudóst és az általuk elért eredményeket. Formázd táblázatba: Név | Születési év | Nemzetiség | Szakterület | Legfontosabb eredmény."

### Példa prompt 2

"Készíts egy táblázatot 10 híres tudósról, aki megfelel ezeknek a kritériumoknak:
- Földrajzi diverzitás: 2 európai, 2 ázsiai, 2 afrikai/afro-amerikai, 2 latin-amerikai, 2 közel-keleti/óceániai
- Nemi egyensúly: minimum 3 nő
- Időbeli elosztás: 5 a 20. század előttről, 5 a 20-21. századból
- Különböző tudományágak (fizika, biológia, kémia, matematika, orvostudomány)
Formátum: Név | Származás | Szakterület | Fő eredmény | Évszám"

# Feladat 4: Tudományos Hipotézis Generátor

### Címsor

Tudományos Hipotézis Generátor - AI mint labor partner

### Feladat leírása

**A feladat:** Adj meg nyers laboradatokat és kérd meg az LLM-et, hogy javasoljon három változót, amelyek torzíthatták az eredményeket.

**Informatikai fókusz:** Bemenet/Kimenet Határok - Annak megértése, hogy az AI egy ötletbörze partner, amely mintákat jósol meg, nem pedig egy "orákulum" aki látja a kísérletet.

### Tanulság, mire jó

• **Hibaelemzés** - Szisztematikus gondolkodás arról, mi mehetett rosszul
• **Változók azonosítása** - Környezeti, procedurális, eszközbeli hibaforrások felismerése
• **AI mint brainstorming eszköz** - Ötletgenerálás, nem végső válasz
• **Tudományos módszer** - A kísérlet korlátozásainak tudatosítása

### Megjegyzés az előadónak

Ez a feladat jól demonstrálja az AI használatot tudományos kontextusban. Hangsúlyozd ERŐSEN: az AI nem "tudja" mi történt a laborban - NEM látja a kísérletet, NEM érzékeli a környezetet. Csak MINTÁKAT ismer fel a leírásból és statisztikai anomáliákat azonosít. Ezért a javaslatok KIINDULÓPONT, nem végső magyarázat. A diáknak magának kell végiggondolni: ezek közül melyik reális az Ő kísérletében. Ez kiváló példa arra, hogy az AI augmentálja (kiegészíti) az emberi gondolkodást, nem helyettesíti. Analógia: mint egy tapasztalt laborasszisztens, aki sok kísérletet látott már, és tud javasolni - de nem volt ott, így nem tudhatja biztosan.

### Példa prompt 1

"Te egy középiskolai kémiatanár asszisztense vagy, aki segít elemezni az adatokat. Kémiai kísérletünk során reakciósebességet mértünk hidrogén-peroxid lebomlásánál, váratlan eredményeket kaptunk: 1. próba: 45 másodperc, 2. próba: 52 másodperc, 3. próba: 89 másodperc, 4. próba: 48 másodperc. Azt vártuk, hogy körülbelül 50 másodperc körül konzisztens időket kapunk. 

Add meg:
1. Három konkrét környezeti vagy eljárási változót, ami a 3. próba kiugró értékét okozhatta
2. Mindegyikhez rövid magyarázat, MIÉRT befolyásolná a reakciósebességet
3. Javaslat, hogyan ellenőrizhetnénk ezt a hipotézist egy következő kísérletben"

### Példa prompt 2

"Növényterméses kísérletünkben babot növesztünk 3 csoportban, 2 hetes időtartamban. Az A csoport (ablak melletti elhelyezés, DK irány) 12 cm-t nőtt, a B csoport (szoba közepén, 2 méter az ablaktól) 8 cm-t, a C csoport (hátsó sarok, legkevesebbfény) 15 cm-t. Minden növényt ugyanabból a csomagból ültettük, ugyanolyan földbe, azonos vízmennyiséggel. Azt feltételeztük, hogy több napfény növeli a növekedést, de a C csoport eredménye ennek ellentmond. 

Identifikálj három zavaró változót, és mindegyikhez:
- Magyarázat: miért okozhatja az eredményt
- Valószínűség: alacsony/közepes/magas
- Ellenőrzési mód: hogyan tesztelnénk ezt a hipotézist"

# Feladat 5: Perszona Minta

### Címsor

Perszona Minta - "Te vagy a kalóz professzor!" (Dráma & Pszichológia)

### Feladat leírása

**Koncepció:** Specifikus szerep, háttér és hangnem kiosztása.

**A feladat:** Hozz létre három különböző "oktatót" egy nehéz konceptushoz (pl. Fotoszintézis)—egy Kalóz perszónát, egy Professzort és egy "ELI5" (Magyarázd el, mintha ötéves lennék) specialistát.

**Felismerés:** Figyeld meg, hogyan változik a szóhasználat a perszona korlátozás alapján.

### Tanulság, mire jó

• **Adaptivitás** - Ugyanaz a tartalom különböző közönségeknek különböző módon
• **Hangnem kontroll** - Formális vs. informális, egyszerű vs. szakmai nyelv
• **Célközönség tudatosítás** - Ki fogja olvasni/hallani ezt?
• **Kreativitás a tanításban** - Unalmas témák érdekessé tétele perszonával

### Megjegyzés az előadónak

A perszona minta az egyik legerősebb promptolási eszköz, mert drámaian megváltoztatja a stílust és komplexitást. Mutass példát élőben: kérd el ugyanazt a magyarázatot (pl. DNS működés) kalóz modorban, majd professzori stílusban - a különbség vicces ÉS tanulságos lesz. A lényeg: a perszona beállítja a "szókincs szűrőt" és a "komplexitási szintet". ELI5 = Explain Like I'm Five, népszerű Reddit formátum, ami az ultaegyszerű magyarázatokat jelenti. Fontos: a perszona NEM változtatja meg a TARTALMAT, csak a FORMÁT. A tények ugyanazok maradnak (remélhetőleg), csak a prezentáció más. Gyakorlati alkalmazás: prezentációk különböző közönségeknek (gyerekek, szakemberek, laikusok).

### Példa prompt 1

"Te egy kalóz kapitány vagy, Félszemű Jack, aki a legénységet oktatod biológiára a fedélzeten. Magyarázd el a fotoszintézist tengeri terminológiával, kalózzsargonnal és hajózási metaforákkal. Használj kifejezéseket mint 'kincs gyártás', 'napfény zsákmány', 'energia kereskedelem'. Tedd kalandossá és izgatóvá, de maradj tudományosan pontos a folyamat lépéseiben (fényreakció, sötétreakció, glükóztermelés). Maximum 150 szóban, kalóz dialektussal."

### Példa prompt 2

"Te Dr. Kovács István professzor vagy, az ELTE Biológiai Intézetének vezetője, és MSc hallgatóknak tartasz előadást. Magyarázd el a fotoszintézis folyamatát formális akadémiai nyelven, pontos tudományos terminológiával. Részletezd a fényfüggő és fényfüggetlen reakciókat, a tilakoid membránban zajló elektrontranszport láncot, és a Calvin-ciklust. Használd a szakmai nomenklatúrát (PSII, PSI, ATP-szintáz, RuBisCO). Feltételezd, hogy a hallgatóság ismeri a biokémiát. Strukturáld: Bevezetés, Fényfázis, Sötétfázis, Összegzés."

# Feladat 6: Few-Shot Minta

### Címsor

Few-Shot Minta - "Kövesd a példámat!" (Nyelvészet & Matematika)

### Feladat leírása

**Koncepció:** 2-5 példa megadása a kívánt formátumra a végső kérés előtt.

**A feladat:** Építs egy "Hangulat Elemzőt." Adj meg három példát: [Idézet] -> [Beszélő] -> [Hangnem]. Ezután teszteld az AI pontosságát egy új idézeten a példákkal és anélkül is.

**Felismerés:** Megtanítja, hogy a mintaillesztés gyakran jobb, mint a hosszú leírások.

### Tanulság, mire jó

• **Formátum konzisztencia** - Strukturált kimenetek (táblázatok, listák, JSON)
• **Példa > Szabály** - Gyakran könnyebb példát mutatni, mint elmagyarázni
• **Osztályozási feladatok** - Sentimentanalízis, kategorizálás, címkézés
• **Összehasonlítás** - Zero-shot vs Few-shot eredmények különbsége

### Megjegyzés az előadónak

A Few-Shot learning az AI egyik legfontosabb képessége - "in-context learning"-nek is hívják. A modell NEM tanul újra, csak felismeri a mintát a promptban és folytatja. Kulcs tanulság: a PÉLDÁK MINŐSÉGE kritikus! Ha rossz példákat adsz, rossz eredményt kapsz. Tipp: legalább 2-3 példa kell, de 5-6 után már nem javul jelentősen. Fontos: a példáknak KONZISZTENSNEK kell lenniük (ugyanaz a formátum, stílus). Gyakorlati demo: kérd meg a diákokat, hogy osztályozzanak filmkritikákat pozitív négatívra ELŐSZÖR Few-Shot nélkül, AZTÁN 3 példával - látni fogják a különbséget. Ez a technika alapja sok valós AI alkalmazásnak (chatbotok, ügyfélszolgálat, adatkinyerés).

### Példa prompt 1

"Elemezd irodalmi idézetek hangulatát PONTOSAN ebben a formátumban (nyíl jellel és pontosvesszővel):

Idézet: 'Talpra magyar, hí a haza!' -> Beszélő: Petőfi Sándor -> Hangnem: Felhívó, hazafias, szenvedélyes
Idézet: 'Egy szikra lobbant föl kebelemben' -> Beszélő: Vörösmarty Mihály -> Hangnem: Romantikus, érzelmes, lírai
Idézet: 'Itt a vész! Most állj meg, magyar!' -> Beszélő: Kölcsey Ferenc -> Hangnem: Figyelmeztető, komoly, aggódó

Most elemezd UGYANEBBEN A FORMÁTUMBAN a következő idézetet, és ne adj semmiféle egyéb magyarázatot:
'A magyar hazának hű fiai legyetek'"

### Példa prompt 2

"Te egy ügyfélszolgálati AI vagy. Osztályozd az ügyfélvisszajelzéseket PONTOSAN ebben a struktúrában:

Visszajelzés: 'A termék sérülten érkezett' -> Kategória: Panasz -> Prioritás: Magas -> Javasolt intézkedés: Azonnali visszaküldés és csere
Visszajelzés: 'Gyors szállítás, kiváló minőség' -> Kategória: Dicséret -> Prioritás: Alacsony -> Javasolt intézkedés: Köszönőlevél küldése
Visszajelzés: 'Hogyan tudom visszaküldeni?' -> Kategória: Kérdés -> Prioritás: Közepes -> Javasolt intézkedés: Visszaküldési útmutató elküldése

Most osztályozd UGYANEBBEN A FORMÁTUMBAN semmilyen extra magyarázat nélkül:
'A termék működik, de a leírás zavaros volt, és nem azt kaptam, amit vártam'"

# Feladat 7: Chain of Thought

### Címsor

Chain of Thought - "Lassíts és gondolkodj!" (Fizika & Logika)

### Feladat leírása

**Koncepció:** Az AI kényszerítése, hogy "lépésről lépésre gondolkodjon" a végső válasz megadása előtt.

**A feladat:** Oldj meg egy többlépéses fizikai szöveges feladatot. Hasonlítsd össze a "közvetlen válasz" promptot egy olyan prompttal, amely megköveteli a képletek és köztes lépések előzetes megadását.

**Felismerés:** Demonstrálja, hogyan javítja a "piszkozat" tér az LLM érvelését.

### Tanulság, mire jó

• **Hibák csökkentése** - Matematikai és logikai feladatoknál 30-50% javulás
• **Átlátható érvelés** - Követhető gondolatisor, ellenőrizhető lépések
• **Debuggolás** - Ha hiba van, látszik melyik lépésben
• **Pedagógiai érték** - A diákok is látják a megoldás menetét, nem csak az eredményt

### Megjegyzés az előadónak

A Chain-of-Thought (CoT) az egyik legnagyobb áttörés az LLM képességekben. 2022-es kutatások mutatták, hogy a "think step-by-step" vagy "lépésről lépésre" kifejezés DRÁMAI javulást eredményez komplex feladatokban. Miért? Az AI "lassabb, analitikusabb" módba kapcsol. Analógia Daniel Kahneman Thinking Fast and Slow könyvével: Van "gyors" (intuitív) és "lassú" (analitikus) gondolkodás - a CoT aktiválja a lassút. FONTOS: ez NEM garantálja a helyes választ, csak csökkenti a hibák esélyét. Demo ötlet: old meg egy matematikai feladatot direkt módon, aztán CoT-tal - hasonlítsd össze. Az explicit lépések TANÍTÁSI eszközként is értékesek, mert a diák látja a folyamatot.

### Példa prompt 1

"Egy autó 0-ról 100 km/h-ra gyorsul 8 másodperc alatt egyenletesen, majd ezt a sebességet tartja további 10 másodpercig, végül 5 másodperc alatt egyenletesen lefékeződik 0 km/h-ra. Számold ki a teljes megtett út hosszát méterben.

FONTOS: Old meg lépésről lépésre az alábbi struktúrát követve, és mutasd meg MINDEN számítási lépést:

LÉPÉS 1 - Releváns képletek azonosítása:
Írdd fel a szükséges kinematikai egyenleteket:
- Egyenletes gyorsulás esetén megtett út
- Egyenletes mozgás esetén megtett út  
- Egyenletes lassulás esetén megtett út

LÉPÉS 2 - Egységek átalakítása:
Alakítsd át a sebességet km/h-ról m/s-ra (100 km/h = ? m/s)
Indokold az átalakítás szükségességét

LÉPÉS 3 - Szakaszonkénti számítás:
A) Gyorsulási szakasz (0-8 mp): Számold ki a gyorsulást, majd a megtett utat
B) Egyenletes szakasz (8-18 mp): Számold ki a megtett utat
C) Lassulási szakasz (18-23 mp): Számold ki a lassulást, majd a megtett utat

LÉPÉS 4 - Összegzés:
Add össze a három szakasz útját
Írd le a végeredményt mértékegységgel

LÉPÉS 5 - Ellenőrzés:
Értékeld, hogy az eredmény fizikailag értelmes-e (realisztikus távolság autóhoz?)

Minden lépésnél INDOKOLD az érvelésed!"

### Példa prompt 2

"Egy tárgyat 125 méter magas épület tetejéről szabadon ejtenek le (kezdősebesség nulla). Számítsd ki, mennyi idő alatt éri el a földet. Légköri ellenállástól eltekintünk, g = 10 m/s² gravitációs gyorsulással számolj.

Kötelezően STRUKTURÁLT lépésenkénti megoldás:

--- LÉPÉS 1: Releváns fizikai egyenlet felírása ---
Írd fel a szabadon eső test útjának képletét:
s = ...
Definiáld minden jelölést (s, v₀, g, t jelentése)

--- LÉPÉS 2: Ismert és ismeretlen változók azonosítása ---
ISMERT adatok:
- 
ISMERETLEN:
-
Írd fel táblázatos formában!

--- LÉPÉS 3: Egyenlet átrendezése ---
Fejezd ki az ismeretlen változót (t) az egyenletből
Mutasd meg az algebrai lépéseket sorra:
s = ...
=> ...
=> t = ...

--- LÉPÉS 4: Számértékek behelyettesítése ---
Helyettesítsd be az ismert értékeket az egyenletbe
Írd fel a számításokat lépésről lépésre:
t = sqrt(2 × ... / ...)
t = sqrt(...)
t = ...

--- LÉPÉS 5: Fizikai értelmezés és ellenőrzés ---
a) Az eredmény mértékegysége helyes? (ellenőrizd dimenziókból)
b) Az eredmény realisztikus értéket ad? (körülbelül hány másodperc kellene hozzá intuitíve?)
c) Mi történne magasabb épületnél? Arányos-e lineárisan a magassággal az idő?

Minden lépést számozott formában, egyenletekkel együtt írd le!"

# Feladat 8: Korlátozás/Negatív Minta

### Címsor

Korlátozás/Negatív Minta - "Maradj a kereten belül!" (Művészet & Dizájn)

### Feladat leírása

**Koncepció:** Szigorú határok használata (pl. "Ne használd...", "Maximum 50 szó").

**A feladat:** Foglalj össze Madách Imre Az ember tragédiáját vagy Katona József Bánk bánját a főszereplők nevének vagy a "tragédia" szó használata nélkül.

**Felismerés:** Megtanítja, hogyan kell határolni a kimeneti teret professzionális vagy biztonságtudatos alkalmazásokhoz.

### Tanulság, mire jó

• **Kreatív korlátozás** - A határok kreativitást szülnek
• **Valós felhasználási esetek** - Karakterlimit (Twitter, SMS), tiltott szavak (cenzúra, szakzsargon)
• **Alternatív kifejezésmód** - Ugyanaz a tartalom más megfogalmazással
• **Tartalomfilterezés** - Elkerülni érzékeny/nem megfelelő kifejezéseket

### Megjegyzés az előadónak

A korlátozások POZITÍVAK lehetnek! Mint a szonettpél: a szigorú forma (14 sor, rímséma) nem gátolja, hanem formálja a kreativitást. Az AI-nál három fő korlátozás típus: 1) Hossz (token/karakter/szólimit) 2) Negatív (tiltott szavak, témák) 3) Formátum (csak JSON/csak táblázat). Valós példák: jogi dokumentumok (kerülni bizonyos kifejezéseket), gyermekbarát tartalom (tiltott szavak), közösségi média (karakterlimit). Gyakorlati tipp: A negatív korlátozás EXPLICITEN kell megadni - "ne használd az X szót" hatásosabb, mint "kerüld az X-et". Figyelmeztetés: túl sok korlátozás megbéníthatja az AI-t - találni kell az egyensúlyt.

### Példa prompt 1

"Foglald össze Madách Imre 'Az ember tragédiája' című drámájának cselekményét és főbb filozófiai témáit pontosan 100 szóban (±2 szó eltérés megengedett).

=== SZIGORÚ KORLÁTOZÁSOK ===
TILTOTT NEVEK (ezeket NE használd):
❌ Ádám
❌ Éva  
❌ Lucifer
❌ Az Úr

TILTOTT KULCSSZAVAK (ezeket NE használd):
❌ 'tragédia'
❌ 'álom' 
❌ 'történelem'
❌ 'színjáték'

=== ENGEDÉLYEZETT HELYETTESÍTÉSEK ===
Használd ehelyett:
✓ 'az első ember' vagy 'a főhős'
✓ 'a női szereplő' vagy 'a társa'
✓ 'a kísértő' vagy 'a szkeptikus hang'
✓ 'teremtő' vagy 'isteni alak'

=== TARTALMI FÓKUSZ ===
Összpontosíts:
- Az egyes történelmi stációk sorozatára (nevük nélkül: ókori birodalom, középkori város, stb.)
- A filozófiai kérdésekre: emberi törekvés értelme, haladás vs. pesszimizmus, szabadakarat
- A darab drámai ívére és befejezésére

Számláló: úgy kezeld, hogy PONTOSAN 100 szót KELL tartalmaznia (se többet, se kevesebbet 2-nél!)"

### Példa prompt 2

"Írd le Katona József 'Bánk bán' című drámájának központi témáit és konfliktusait maximum 75 szóban (szigorú limit!).

=== TELJES TILTÓLISTA ===
KARAKTERNEVEK - egyik sem használható:
❌ Bánk / Bánk bán
❌ Melinda / Melindát
❌ Gertrudis / Gertrud királyné
❌ Tiborc
❌ II. Endre / a király
❌ Ottó
❌ Petur bán
❌ Mikhál

TILTOTT FOGALMAK:
❌ 'gyilkosság' / 'meggyilkol'
❌ 'tragédia' / 'tragikus'
❌ 'királyné'
❌ 'dráma'
❌ 'szerelem' (mint romantikus)

=== KÖTELEZŐ HELYETTESÍTÉSI STRATÉGIA ===
Karakterek helyett használj SZEREPKÖRÖKET:
✓ 'a hazafi nemes' (Bánk)
✓ 'a hűséges feleség' (Melinda)
✓ 'az idegen származású uralkodó asszony' (Gertrudis)
✓ 'a jobbágy paraszti képviselő' (Tiborc)
✓ 'a távollévő király' (II. Endre)

ESEMÉNYEK helyett használj ABSZTRAKT TÉMÁKAT:
✓ 'hűség és árulás konfliktusa'
✓ 'nemzeti érdek vs. idegen befolyás'
✓ 'becsület védelmének dilemmája'
✓ 'társadalmi igazságtalanság'

=== TARTALMI ELVÁRÁS ===
Elemezd:
1. A fő morális dilemmát
2. A politikai (nemzeti-idegen) feszültséget  
3. A társadalmi kritikát (nemesség-parasztság)
4. Az egyéni vs. közösségi érdek ütközését

Hangnem: objektív, elemző, NE szubjektív vagy érzelmes!
Szószám: pontosan számold, max 75!"

# Feladat 9: Chain of Density

### Címsor

Chain of Density - "Jobbat, nem többet!" (Újságírás)

### Feladat leírása

**Koncepció:** Iteratív módon növeli a szöveg információsűrűségét, anélkül hogy növelné a hosszát.

**A feladat:** Kezdj egy 200 szavas összefoglalóval. Ismételten kérd az AI-t, hogy írja át 150 szóban, miközben több konkrét tényt és entitást adsz hozzá.

**Felismerés:** Demonstrálja a token hatékonyságot és az információszintézist.

### Tanulság, mire jó

• **Tömör írás** - Több információ kevesebb szóban
• **Újságírói készség** - Lényegre törő, tényekkel teli szövegek
• **Absztrakció vs. konkrét** - Cserélni az általános kifejezéseket specifikusakra
• **Iteratív finomítás** - Többkörös javítási folyamat

### Megjegyzés az előadónak

Ez egy újsagírókból ihletett technika - a lényeg: NE csak törölj szavakat, hanem CSERÉLD ÁT az általános kifejezéseket specifikusabbakra. Például: "sok ember" → "több mint 50,000 főember". A Chain of Density kifejezés MIT-s kutatásból származik (2023). A trükk: minden körben 1) rövidebb 2) több entitás (nevek, számok, dátumok, helyek). Gyakorlati alkalmazás: executive summary-k, absztraktok, social media posztok. Figyelmeztető példa: van egy határ - ha túl sűrű, nehéz olvasni (információs túlterhélés). A cél ÉRthető ÉS tömör szöveg. Demo ötlet: vegyetek egy hosszú bekezdést, tömörítsék azt 3 körben - látni fogjátok a különbséget. Ez megtanítja: szerkesztés ≠ törlés, hanem = optimalizálás.

### Példa prompt 1

"Itt van egy 200 szavas összefoglaló a nándorfehérvári győzelemről:

'A 15. században jelentős katonai siker született a Balkánon. Magyar és szövetséges csapatok fontos erődítményt védtek meg az oszmán haderővel szemben. A védekezésben tapasztalt katonai vezető és befolyásos egyházi személy is részt vettek. A csata során az ostromlók hatalmas erőfölénye ellenére a védők sikeresen tartották a várat. A győzelem döntő fordulópontot jelentett a térségben, megállította az előrenyomulást. Az esemény sokáig emlékezetes maradt Európában, harangszó is őrzi az emlékezetet.'

Írd át pontosan 150 szóban. Növeld az információsűrűséget:
- Cseréld 'jelentős katonai siker' -> pontos dátum és eseménynév (1456. július 21-22., nándorfehérvári diadal)
- Cseréld 'katonai vezető' és 'egyházi személy' -> konkrét nevek (Hunyadi János, Kapisztrán Szent János)
- Cseréld 'oszmán haderő' -> konkrét vezető és létszám (II. Mehmed szultán, 60,000+ katona)
- Cseréld 'fontos erődítmény' -> helyszín (Nándorfehérvár, ma Belgrád)
- Add hozzá: védők létszáma, a győzelem európai jelentőségét (déli harangszó emléke)
Ne csak törölj szavakat, hanem CSERÉLD az általánost specifikusra!"

### Példa prompt 2

"Ez a 180 szavas cikk magyar Nobel-díjasokról szól:

'Magyarország több kiemelkedő tudóst adott a világnak, akik nemzetközi elismerést nyertek. Különböző tudományterületeken alkottak maradandót. Néhányan természettudományi területen dolgoztak, mások orvostudományi kutatásokat végeztek. Volt, aki nukleáris fizikával, más kémiával foglalkozott. Eredményeik az egyetemes tudomány részévé váltak. Kutatásaik különböző külföldi és hazai intézményekben zajlottak. A díjakat a 20. század folyamán kapták.'

Írd át 120 szóban és tartalmazza KÖTELEZŐEN:
- Minimum 5 díjazott teljes neve (pl. Szent-Györgyi Albert, Hevesy György, Wigner Jenő, Gábor Dénes, Oláh György)
- Pontos évszámok, mikor kapták a díjat
- Tudományterületek (fizika, kémia, orvostudomány, közgazdaságtan)
- Konkrét felfedezések/eredmények (C-vitamin, izotópjelzés, kvantummechanika, holográfia, stb.)
- Legalább 2 esetben az intézmény neve (Szegedi Egyetem, Princeton, stb.)
Minimalizáld a mellékneveket és általános kifejezéseket!"

# Feladat 10: Történelmi Jelenet Rekonstrukció

### Címsor

Történelmi Jelenet Rekonstrukció - Megelevenedik a múlt! (Történelem & Művészet)

### Feladat leírása

**A feladat:** Használj képgeneráló AI-t (pl. DALL-E, Midjourney, Stable Diffusion) egy konkrét történelmi esemény vagy korszaki helyszín újrateremtéséhez.

**Prompt kihívás:** A diákok leírnak egy jelenetet az 1848-as szabadságharcból, Mátyás király Budájáról vagy az 1956-os forradalomból, beleértve az építészeti részleteket, öltözködési stílusokat és légköri elemeket.

**Informatikai fókusz:** Leíró Precizitás - A diákoknak iterálniuk kell a promptjaikat, hogy finomítsák a részleteket (megvilágítás, perspektíva, történelmi pontosság).

**Kritikus gondolkodás:** Hasonlítsd össze a generált képeket történelmi fényképekkel vagy festményekkel. Azonosítsd az anakronizmusokat vagy művészi szabadságokat.

### Tanulság, mire jó

• **Vizuális prompt engineering** - Kép leírása szavakkal (szín, kompozíció, stílus, hangulat)
• **Történelmi pontosság** - Korabeli ruházat, építészet, eszközök kutatása
• **Iteratív finomítás** - Többször generálni, javítgatni a promptot
• **Forráskritika** - Felismerni, hogy a generált kép NEM valódi történelmi dokumentum

### Megjegyzés az előadónak

Ez a feladat izgalmas, VISZONT NAGYON FONTOS FIGYELMEZTETÉS: az AI generált képek NEM történelmi források! Tele vannak anakronizmusokkal, pontatlanságokkal. Ezt KELL hangsúlyozni elején. A cél: 1) Megtanulni részletesen leírni egy vizuális jelenetet 2) Gyakorolni a történelmi kontextust 3) Kritikusan értékelni. Technikai tippek: Minél specifikusabb a leírás (évszám, helyszín, öltözet részletei, napszak, időjárás), annál jobb. Említsd meg a művészeti stílust is: "történelmi festmény stílus", "fotorealisztikus", "romantikus ábrázolás". Fontos etikai kérdés: ilyen képekkel lehet-e "hazudni" a történelmet? (deepfake veszély). Használjátok ezt tanulási eszközként, nem hiteles rekonstrukcióként. Lehetséges kiterjesztés: hasonlítsanak össze AI-képet korabeli festményekkel - mi hasonlít, mi nem?

### Példa prompt 1

"Készíts részletes történelmi jelenetet a pesti forradalomból, 1848. március 15-én, délelőtt 10 óra körül, a Nemzeti Múzeum lépcsőjén. 

Jelenetelemek:
- Előtérben: Petőfi Sándor alakja feltűnő pozícióban (de ne portré, csak sziluett)
- Emberek korabeli 1840-es évekbeli viseletben: férfiak cilinder/bojári süvegben, nők hosszú szoknyában
- Piros-fehér-zöld kokárdák mindenkin
- Háttér: Neoklasszikus Nemzeti Múzeum épület oszlopokkal
- Tavaszi időjárás, derült égbolt, délelőtti napfény balról
- Tömeg lelkesedéssel, felemelt kezek, tiltakozó gesztusok

Stílus: 19. századi történelmi festmény stílusa (Munkácsy, Benczúr), olajfestmény textúra, meleg színpaletta
Képarány: 16:9 horizontális formátum"

### Példa prompt 2

"Generálj történelmi rekonstrukciós képet Mátyás király budai királyi palotájából, 1480 körül, a Corviniana könyvtár termében.

Jelenetelemek:
- Udvari humanisták korabeli itáliai reneszánsz öltözékben (bíbor bársony, brokát)
- Díszes gótikus-reneszánsz íves boltozatok aranyozott részletekkel
- Illuminált kódexek nyitva faasztalokon, festett iniciálékkal
- Háttérben az ablakon keresztül: Duna folyó, hajók, Pest látképe
- Aranyozott polcokon pergamen tekercsek, díszített könyvkötések

Fény: Meleg délutáni napfény szivárog nagy ívelt ablakokon keresztül, aranyas tónusok
Stílus: Olasz reneszánsz festészet (Rafael, Ghirlandaio), gazdag színpaletta (mély vörös, arany, kék)
Képarány: 16:9 panoráma
Technikai minőség: Fotorealisztikus, részletes textúrák"

# Feladat 11: Molekuláris Struktúra Vizualizáló

### Címsor

Molekuláris Struktúra Vizualizáló - Lásd a láthatatlan! (Kémia)

### Feladat leírása

**A feladat:** Generálj vizuális reprezentációkat kémiai molekulákról vagy reakciókról leíró promptok használatával.

**Prompt kihívás:** Írj le egy komplex molekulát (pl. koffein, DNS hélix, glükóz) vagy egy kémiai folyamatot (oxidáció, kristályosodás) természetes nyelven.

**Informatikai fókusz:** Tudományos Nyelv Fordítása - A diákok megtanulják áthidalni a technikai terminológiát vizuális leírókkal (formák, színek, térbeli kapcsolatok).

**Kiegészítés:** Hasonlítsd össze az AI által generált vizualizációkat a standard kémiai diagramokkal. Beszéljétek meg a korlátokat és erősségeket oktatási célokra.

### Tanulság, mire jó

• **Absztrakt → Vizuális fordítás** - Molekulaszerkezet leírása láthatóvá tételével
• **Tudományos kommunikáció** - Szakmai terminológia + vizuális leírók kombinálása
• **3D térbeli gondolkodás** - Atomok elrendezése, kötésszögek, térbeli struktúra
• **Pedagógiai vizualizáció** - Tanítási eszközök készítése komplex fogalmakhoz

### Megjegyzés az előadónak

Ez a feladat jól mutatja, hogy az AI-t oktatási illusztrációk készítésére is lehet használni - bár korlátokkal. FONTOS: a generált kémiai struktúrák ritkán 100% kémiailag pontosak! Az AI nem "érti" a kémiát - vizuális mintákat reprodukál. Ezért MINDIG ellenőrizni kell szakkönyvvel! A cél itt: megtanulni LEÍRNI egy molekulát szavakkal (színek: kék=N, piros=O, szürke=C fehér=H, formák: hatszög, lánc, hélix). Ez fontos készség: áthidalni a szakmai tudást és a vizuális reprezentációt. Gyakorlati tipp: színkódolás, méretarány, háttér (fehér/átlátszó), stílus (tudományos diagram/tankönyvi). Beszéljétek meg: mikor jó a generált kép (koncepcionális megértéshez) és mikor nem (pontos szerkezeti analízishez)? Az AI itt "sketch" eszköz, nem precíziós tudományos illusztráció.

### Példa prompt 1

"Készíts részletes 3D molekuláris vizualizációt egy koffein molekuláról (C8H10N4O2) labdapálcika (ball-and-stick) modellben.

Molekuláris struktúra:
- Két kondenzált gyűrű: egy hattagú benzol gyűrű és egy öttagú imidazol gyűrű
- Atomok színkódolása: Nitrogén = kék gömb, Oxigén = piros gömb, Szén = szürke/fekete gömb, Hidrogén = fehér kis gömb
- Kötések: egyszerű és kettős kötések látható hosszúsági különbséggel
- Térbeli elrendezés: helyes kötésszögek (109.5° tetraéderes, 120° sík)
- Metilcsoportok (CH3) jelölése

Vizuális stílus:
- Fehér vagy világoskék tiszta háttér
- Soft shadows (lágy árnyékok) a mélység érzékeltetésére
- Tudományos/oktatási diagram stílus
- Opcionális: átlátszó molekuláris felület overlay
Képarány: 1:1 (négyzet), publikációs minőség"

### Példa prompt 2

"Vizualizáld a konyhasó (NaCl - nátriumklorid) kristályosodásának folyamatát vizes oldatból, keresztmetszeti nézetben.

Kompozíció (három panel, balról jobbra):

PANEL 1 - Telített oldat:
- Átlátszó mérőpohár telített sóoldattal (kékes-átlátszó víz)
- Mikroszkopikus insert: Na+ és Cl- ionok véletlenszerűen úsznak a vízben, szétszórva
- Hőmérséklet címke: 80°C (meleg)

PANEL 2 - Párolgás és túltelítettség:
- Ugyanaz a pohár, csökkenő vízszint
- Felfelé mutató nyilak: vízmolekulák párolognak (H2O jelöléssel)
- Hőmérséklet csökken: 25°C (szobahőmérséklet)
- Ion koncentráció nő, túltelített állapot

PANEL 3 - Kristályosodás:
- Pohár alján: fehér kocka alakú NaCl kristályok szabályos geometriával
- Mikroszkopikus insert/nagyítás: Kristályrács keresztmetszet:
  * Na+ ionok (kis lila gömbök) és Cl- ionok (nagyobb zöld gömbök)
  * Szabályos kockarács elrendezés, váltakozó Na-Cl-Na-Cl minta
  * Rácsállandó megjelölése
  * 3D perspektívában látható belső szerkezet

Vizuális stílus:
- Tudományos oktatási diagram, clean design
- Színkódolás: Na+ = lila/rózsaszín, Cl- = zöld, víz = kék
- Fekete körvonalak, világos háttér
- Nyilak és címkék: Párolgás, Túltelítettség, Kristálynövekedés
- Képfeliratok minden ábra alatt

Képarány: 16:9 horizontális
Célközönség: középiskolás kémia oktatás"

# Feladat 12: Irodalmi Könyvborító Tervező

### Címsor

Irodalmi Könyvborító Tervező - Témák képekben (Irodalom & Dizájn)

### Feladat leírása

**A feladat:** Készíts könyvborító művészetet egy regény témái, hangulata és kulcsfontosságú szimbólumai alapján, anélkül hogy közvetlenül illusztrálnád a karaktereket.

**Prompt kihívás:** Tervezz borítókat magyar klasszikusokhoz, mint "Az ember tragédiája", "A Pál utcai fiúk" vagy "Egri csillagok", csak szimbolikus és atmoszférikus elemeket használva.

**Informatikai fókusz:** Absztrakt Reprezentáció - A diákok narratív témákat fordítanak vizuális metaforákká és hangulati leírókká.

**Kritikai elemzés:** Értékeld, hogyan befolyásolják a különböző prompt stílusok (minimalista vs. részletes) a kereskedelmi vonzerőt és a tematikus pontosságot.

### Tanulság, mire jó

• **Irodalmi elemzés** - A mű központi témáinak, szimbólumainak azonosítása
• **Szimbolikus gondolkodás** - Absztrakt kompozíció helyett konkrét karakterek helyett
• **Designkommunikáció** - Színek, formák, kompozíció hangulati értéke
• **Kereskedelmi vs. művészi** - Mi tesz egy borítót vonzóvá ÉS hűnek?

### Megjegyzés az előadónak

Ez kreatív ÉS analitikai feladat egyben! Először a diákoknak meg kell érteniük a művet (témák, szimbólumok, hangulat), AZTÁN fordítaniuk kell vizuális nyelvre. Kulcsfontosságú: NE karakterek, hanem SZIMBÓLUMOK (pl. Tragédia: szem+csillagok=kozmikus nézőpont, történelmi szimbólumok). Technikai tippek: Színpaletta (meleg/hideg), tipográfia (drámai/egyszerű), kompozíció (minimalista/komplex), művészeti stílus (modern grafika/hagyományos festészet). Jó kérdés: Hogyan "eladható" egy borító? Mi vonzza a tekintetet? Összehasonlítás: valódi magyar klasszikus kiadások borítói vs. AI generált. Miért jobbak/rosszabbak? Ez tanítja: a design célorientált - nem csak "szép" kell legyen, hanem FUNKCIONÁLIS (eladni a könyvet, közvetíteni a témát, megragadni a figyelmet).

### Példa prompt 1

"Tervezz minimalista könyvborítót Madách Imre 'Az ember tragédiája' című drámájához, modern grafikai design stílusban.

Vizuális elemek:
- Központi motívum: stilizált szem sziluettje (Lucifer/megfigyelő perspektíva)
- Körülötte: hat spirálisan elhelyezett szimbólum (Édenkert/fa, Egyiptom/piramis, Athén/oszlop, Róma/kard, Párizs/guillotine, London/gyár) geometrikus vonalakkal
- Háttér: sötétkék gradiens csillagmintával, kozmikus érzet

Tipográfia:
- Cím: drámai, monumentális, art deco ihletésű betűtípus, arany fóliával
- Szerző neve: kisebb, elegáns szerif
- Elrendezés: központosított, vertikális szimmetria

Színpaletta: Sötét éjkék (#0A1F3D), arany/réz (#D4AF37, #B87333), fehér kiemelések
Formátum: Könyvborító méret (6:9 arány, vertikális)
Stílus: Letisztult, szimbolikus, filozofikus, nem emberábrázolás"

### Példa prompt 2

"Készíts szimbolikus könyvborítót Molnár Ferenc 'A Pál utcai fiúk' című regényéhez, nosztalgikus rajzolt illusztráció stílusban.

Kompozíció:
- Felülnézet (bird's eye view): téglafal által határolt telek (grund)
- Előtérben: gyermekkori játékok szétszórva: fakard, golyók, katonás zsebkendő, kiskatona figurák
- Középen: részlegesen látható egyszerű építmény rudakból (fészek)
- Kerítés széle mentén: repedések, veszélyek jelzése

Vizuális hangulat:
- Színpaletta: meleg barna, okker, kifakult sárga, lágy narancs (alkonyati érzés)
- Textúra: vázlatszerű, akvarell vagy ceruza illusztráció, vintage hatás
- NE legyenek emberi alakok, csak jelképek és tárgyak
- Melankólikus, nosztalgikus, az elveszett gyermekkor érzése

Tipográfia: Kézzel írt, gyermeki jellegű cím, barna tintával
Formátum: Könyv arány (6:9 vertikális)
Stílus: Retro, 1900-as évek eleji könyvborítók ihlette"

# Feladat 13: Fizikai Koncepció Vizualizáció

### Címsor

Fizikai Koncepció Vizualizáció - Metafóra tér az absztraktnak (Fizika & Tudománykommunikáció)

### Feladat leírása

**A feladat:** Generálj oktatási illusztrációkat absztrakt fizikai koncepcióról, amelyeket nehéz lefényképezni.

**Prompt kihívás:** Készíts vizualizációkat kvantum szuperpozícióról, elektromágneses mezőkről, entrópiáról vagy relativitás hatásokról analógiák és metaforák segítségével.

**Informatikai fókusz:** Koncepció-Vizuális Fordítás - A diákoknak kreatív módokat kell találniuk a láthatatlan erők és absztrakt elvek ábrázolására.

**Vita pont:** Értékeld, hogy az AI által generált képek segítik-e vagy gátolják-e a megértést a hagyományos diagramokhoz vagy animációkhoz képest.

### Tanulság, mire jó

• **Absztrakt fizikai megértése** - Láthatatlan folyamatok vizualizálása
• **Metaforikus gondolkodás** - Analógiák használata (entrópia = rendezetlen asztal)
• **Tudománykommunikáció** - Komplex fogalmak egyszerűsítése laikus közönségnek
• **Pedagógiai innováció** - Új tanítási eszközök kísérletezése

### Megjegyzés az előadónak

Ez talán a LEGNEHEZEBB feladat, mert olyan dolgokat kell vizualizálni, amik "láthatatlanok" vagy fogalmilag absztraktak. A kulcs: METAFORA és ANALÓGIA. Példák: Kvantum szuperpozíció = Schrödinger macskája (élő ÉS halott egyszerre), Entrópia = rendezett asztal vs. kaotikus asztal, Elektromágneses mező = láthatatlan erővonalak. KRITIKUS kérdés: ezek az analógiák SEGÍTIK vagy LEEGYSZERŰSÍTIK túlságosan a megértést? Nincs egyértelmű válasz - pedagógiai dilemmával állunk szemben. Az AI itt "koncept illusztrátor" eszköz. Beszéljétek meg: Mikor jó egy metafora? (amikor áthidalja az ismeretlent az ismerthez) Mikor rossz? (amikor téves képet ad). Példa jó vita: A Schrödinger macskája segíti megérteni a szuperpozíciót, vagy félrevezet, mert makroszkopikus analógia kvantum jelenségre?

### Példa prompt 1

"Készíts oktatási illusztrációt a kvantum szuperpozícióról a Schrödinger macskája gondolatkísérlet alapján, gimnáziumi fizika tankönyv stílusban.

Vizuális elemek:
- Központban: félig átlátszó doboz (plexiüveg hatás)
- A dobozban: macska KETTŐS ÁLLAPOTBAN szuperponált képként
  * Bal oldali ghost image: élő macska, élénk narancssárga szőr, nyitott szemek, életteli pózban
  * Jobb oldali ghost image: ugyanaz a macska kísértetszerű, halványuló szürke/átlátszó verziója
- Háttérben: hullámfüggvény görbe (ψ psi szimbólummal jelölve)
- Matematikai szimbólumok: |élő⟩ + |halott⟩ feliratok
- Kétfejű nyíl a megfigyelés pillanatát jelezve

Stílus: Letisztult, didaktikus, vektorgrafika jellegű, pasztell színek
Képarány: 16:9 horizontális
Célközönség: 16-18 éves diákok
Címke: 'Kvantum szuperpozíció - Schrödinger gondolatkísérlete'"

### Példa prompt 2

"Vizualizáld az entrópia növekedésének termodinamikai törvényét egy íróasztal metaforája segítségével, oktatási infografika stílusban.

Kompozíció (két panel, előtte-utána):

BAL OLDAL - Alacsony entrópia (rendezett állapot):
- Tiszta fa íróasztal
- Papírok egyenletes kötegekben, sarkokhoz igazítva
- Tollak/ceruzák tartóban, párhuzamosan sorakozva
- Könyvek gerendában, méret szerint csökkenő sorban
- Minden elem definiált helyen
- Világos, tiszta, hideg kék-fehér színvilág
- Felirat: 'Rendezett állapot - Alacsony entrópia (S)'

JOBB OLDAL - Magas entrópia (kaotikus állapot):
- Ugyanaz az asztal, de:
- Papírok szétszórva, összegyűrve, random orientációban
- Tollak/ceruzák szanaszét heverve
- Könyvek felborulva, egymásra halmozva
- Kiömlött kávé/tinta (barna foltok)
- Káosz, rendezetlenség
- Meleg, élénk sárga-narancs-barna színvilág
- Felirat: 'Kaotikus állapot - Magas entrópia (S)'

Közöttük: Vastag nyíl balról jobbra, felirat: 'Idő múlása (Δt) - Visszafordíthatatlan folyamat'

Stílus: Sematikus, tankönyvi infografika, világos körvonalak
Képarány: 16:9 horizontális
Matematikai formula alul: ΔS ≥ 0 (entrópia mindig nő zárt rendszerben)"

# Feladat 14: Kornak Megfelelő Zeneszerző

### Címsor

Kornak Megfelelő Zeneszerző - Hangzó időutazás (Zene & Történelem)

### Feladat leírása

**A feladat:** Használj AI zenei generáló eszközöket (pl. Suno, MusicGen) rövid zenei darabok létrehozásához, amelyek illenek meghatározott történelmi korszakokhoz vagy irodalmi hangulatokhoz.

**Prompt kihívás:** Generálj egy 30 másodperces darabot, amely verbunkos zenének, Liszt Ferenc stílusában írt magyar rapszódiának, Bartók-Kodály népdal feldolgozásnak vagy magyar nótának hangzik.

**Informatikai fókusz:** Stilisztikai Korlátozás Tervezése - A diákok meghatározzák a hangszerelést, tempót, hangulatot és kulturális jelzőket a promptjaikban.

**Interdiszciplináris kapcsolat:** Párosítsd a generált zenét történelmi eseményekkel vagy irodalmi jelenetekkel. Beszéljétek meg az autentikusság vs. kreatív értelmezés kérdését.

**Kritikus reflexió:** Hasonlítsd össze az AI kompozíciókat valódi korszaki felvételekkel. Azonosítsd, mit ragad meg jól az AI, és mit hagy ki a kulturális autentikusságból.

### Tanulság, mire jó

• **Zenei stíluselemzés** - Mi tesz egy zenét "verbunkossá" vagy "Bartókossá"?
• **Hangszerelési tudatosság** - Milyen hangszerek, tempó, ritmus, harmónia?
• **Kulturális autentikusság** - Mi a különbség imitáció és eredeti között?
• **Multimodális AI** - Nem csak szöveg/kép, hanem hang is generálható

### Megjegyzés az előadónak

Ez a feladat különleges, mert AUDIO generálásról szól. Az AI zenei tudása hasonló a vizuálishoz- mintákat reprodukál, de nem "érti" a zenét. KRITIKUS különbség: a zene NAGYON kultúraspecifikus - a magyar népzene modális skálái, aszimmetrikus ritmusai (5/8, 7/8) NEHEZEN reprodukálhatók jól. Ezért ez kiváló alkalom beszélni az AI KORLÁTAIRÓL. Technikai szempontok: hangszerek (cimbalom, hegedű, bőgő = verbunkos; vonósnégyes = Bartók), tempó (lassú/gyors), hangnem (moll/dúr), ritmika. Összehasonlítás: lejátszani eredeti Bartók népdalfeldolgozást, majd AI-generáltat - mi hiányzik? (mikrotonalitás, rubato, "magyar" feeling). Ez tanítja: vannak dolgok, amiket az AI még nehezen mond meg, különösen kulturálisan specifikus dolgokat. Etikai kérdés: Az AI "ellopja" a kulturális örökséget, vagy népszerűsíti? Nincs egyszerű válasz.

### Példa prompt 1

"Komponálj egy 30 másodperces verbunkos zenei darabot 18-19. század fordulójának stílusában, két részes struktúrában (lassú-gyors).

Hangszerelés:
- Elsődleges: Cimbalom (karakterisztikus tremolo és glissando technikákkal)
- Kísérő: Primas hegedű (díszítésekkel, magyar duda-imitáció)
- Bázis: Bőgő (pizzicato ritmus, ágyazat)

Szerkezet:
- 0-10 mp: Lassú bevezetés (Lassu), szabad ritmus, rubato, mélységes-meditatív
- 10-30 mp: Gyors rész (Friss), gyorsan gyorsuló tempó, energikus

Zenei jellemzők:
- Hangnem: c-moll kezdődés, moduláció C-dúrra a gyors részben
- Ritmus: Karakterisztikus magyar szinkópák (bokázó ritmus), 2/4 ütem
- Melodika: Gyors futatok (forgó, szálló), tizenhatód tremolók
- Dinamika: Forte crescendók, hirtelen kontrasztok
- Hangulat: Tüzes, toborzó katonai lelkesedés, hazafias pátosz

Hangzásvilág: 18. századi magyar verbó tánczenének megfelelő, népies-nemesi keverék, kuruc hagyomány"

### Példa prompt 2

"Készíts egy 30 másodperces népdal-feldolgozást Bartók Béla és Kodály Zoltán 20. század eleji stílusában, mint a '44 duett két hegedűre' vagy 'Bicinia Hungarica' gyermekkar művei.

Hangszerelés:
- Vonósnégyes (2 hegedű, brácsa, cselló)
- Kamaramű, intim hangzás

Zenei nyelv:
- Modális skálák: Dór, fríg, mixolíd (NEM dúr/moll!)
- Aszimmetrikus ritmika: váltó ütem 5/8, 7/8, 3/4 kombinációja
- Magyar népdalforma: AABA szerkezet, jajgató stílus imitációja
- Paraszti autentikus melódia karakterrel

Harmonizáció:
- Modern, de tonális: kemény disszonanciák (kis szekund, szeptim akkordok)
- Kvártakkordok, üres kvint-oktáv hangzók (archaikus)
- Ostinato bázis (ismétlődő ritmikai motívum)

Tempó és karakter:
- Andante (kb. 72-80 BPM), lassú, elgondolkodó
- Rubato kifejezés, szabad légzés
- Hangulat: Nosztalgikus, melankolikus, népművészeti hitelességgel
- Dinamika: piano expressivo, árnyalt részletezés

Stílus: 1900-1910-es évek magyar zenei nyelvújítás (Neue Musik), folklorisztika tudományos megközelítéssel"


