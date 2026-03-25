# Nagy Nyelvi Modellek (LLM-ek) Használata

Gyakorlat, promptolási minták és az átmenet a kérdezéstől az AI-val való együttműködésig.

A standard komponensek, Kontextus-Feladat-Korlátozás modell:

- Perszona: Egy specifikus szerep kiosztása (pl. "Te egy senior adattudós vagy"). Definiálták a "ki"-t?
- Feladat: Egyértelmű, felszólító ige, amely leírja a cselekvést. Egyértelmű-e a cél?
- Kontextus: Háttérinformáció, célközönség vagy releváns adat. Van elég "miért" és "hol"?
- Korlátozások: Korlátok a hosszra, hangnemre vagy tiltott témákra. Határoztak meg határokat?
- Formátum: A kívánt struktúra (Táblázat, JSON, Markdown, Felsorolás). Használatra kész a kimenet?

A "Zero-Shot-tól a Chain-of-Thought-ig" Skála

- 1. Szint: Standard Promptolás (Egyszerű kérdés/utasítás).
- 2. Szint: Few-Shot Promptolás (2-3 példa megadása a prompton belül).
- 3. Szint: Chain-of-Thought (CoT) (Az AI utasítása, hogy "gondolkodjon lépésről lépésre").
- 4. Szint: Iteratív Finomítás (Az AI-t arra kérjük, hogy kritizálja saját korábbi válaszát).
- 5. Szint: Meta-Promptolás (Az AI-t megkérjük, hogy írja meg a legjobb promptot egy adott feladathoz).

Plusz egy: kérd meg az AI-t, hogy értékelje a promptodat, pontozza 1-10 skálán, és javasoljon fejlesztéseket.

Minták Egy Pillantásra

- Perszona: "Ki vagy?", Hangnem, stílus és szakmai zsargon
- Few-Shot: "Kövesd a példám.", Adatformázás és osztályozás.
- Chain of Thought: "Lassíts és gondolkodj.", Logika, matematika és összetett érvelés.
- Korlátozások: "Maradj a határokon belül.", Szigorú projekt követelmények betartása.
- Iteratív Finomítás: "Jobbat, ne többet.", Összefoglalás és professzionális szerkesztés.

Bölcs Használati Ellenőrzőlista Diákoknak

- Szerepjáték: Rendelj hozzá egy perszonát a kontextus beállításához.
- Tényfelderítés: Ellenőrizz legalább egy állítást külső forrás használatával.
- Etikai Ellenőrzés: Keress elfogultságot vagy kizárt csoportokat a kimenetben.
- Hivatkozás: Jelöld egyértelműen az AI által generált részeket a végső munkában.

## Tantárgyközi Kreatív Feladatok

Fókusz: AI Kompetencia, Tényfelderítés és Interdiszciplináris Alkalmazás.

### Történelmi Interjú Feladat (Történelem)

A Feladat: Promptold az LLM-et, hogy egy konkrét történelmi személyként viselkedjen (pl. Széchenyi István vagy Kossuth Lajos).

Informatikai Fókusz: Iteratív Promptolás. A diákoknak finomítaniuk kell a "rendszer promptot" hogy tartalmazzon specifikus korlátozásokat, mint például 19. századi szókincs vagy utalások konkrét reformokra, események a szabadságharcból.

Kritikus Gondolkodás: Hasonlítsd össze az AI válaszokat tankönyvekkel, hogy azonosítsd a hallucinációkat.

### Algoritmikus Költő Feladat (Irodalom)

A Feladat: Generálj egy verset egy meghatározott stílusban (pl. Petőfi vagy Arany János stílusában) egy modern technikai témáról, mint a kiberbiztonság vagy a mesterséges intelligencia.

Informatikai Fókusz: Mintafelismerés. Elemezd, hogyan változtatja meg a kimenetet a stílusbeli kulcsszavak vagy a "hőmérséklet" beállítások módosítása.

### Adat Elfogultság Detektív (Társadalomismeret & Matematika)

A Feladat: Kérj egy listát a "10 híres tudósról" és elemezd az eredményeket demográfiai elfogultság szempontjából.

Informatikai Fókusz: Tanítási Adat Tudatosság. A diákoknak egy "Elfogultság-mentesítő Promptot" kell tervezniük, hogy globálisan reprezentatív kimenetet biztosítsanak.

### Tudományos Hipotézis Generátor

A Feladat: Adj meg nyers laboradatokat és kérd meg az LLM-et, hogy javasoljon három változót, amelyek torzíthatták az eredményeket.

Informatikai Fókusz: Bemenet/Kimenet Határok. Annak megértése, hogy az AI egy ötletbörze partner, amely mintákat jósol meg, nem pedig egy "orákulum" aki látja a kísérletet.

## Prompt Tervezési Minták

Fókusz: AI Interakciók Strukturális Tervezése.

### Perszona Minta (Dráma & Pszichológia)

Koncepció: Specifikus szerep, háttér és hangnem kiosztása.

Feladat: Hozz létre három különböző "oktatót" egy nehéz konceptushoz (pl. Fotoszintézis)—egy Kalózt, egy Professzort és egy "ELI5" (Magyarázd el, mintha ötéves lennék) specialistát.

Felismerés: Figyeld meg, hogyan változik a szóhasználat a perszona korlátozás alapján.

### Few-Shot Minta (Nyelvészet & Matematika)

Koncepció: 2-5 példa megadása a kívánt formátumra a végső kérés előtt.

Feladat: Építs egy "Hangulat Elemzőt." Adj meg három példát: [Idézet] -> [Beszélő] -> [Hangnem]. Ezután teszteld az AI pontosságát egy új idézeten a példákkal és anélkül is.

Felismerés: Megtanítja, hogy a mintaillesztés gyakran jobb, mint a hosszú leírások.

### Chain of Thought Minta (Fizika & Logika)

Koncepció: Az AI kényszerítése, hogy "lépésről lépésre gondolkodjon" a végső válasz megadása előtt.

Feladat: Oldj meg egy többlépéses fizikai szöveges feladatot. Hasonlítsd össze a "közvetlen válasz" promptot egy olyan prompttal, amely megköveteli a képletek és köztes lépések előzetes megadását.

Felismerés: Demonstrálja, hogyan javítja a "piszkozat" tér az LLM érvelését.

### Korlátozás/Negatív Minta (Művészet & Dizájn)

Koncepció: Szigorú határok használata (pl. "Ne használd...", "Maximum 50 szó").

Feladat: Foglalj össze Madách Imre Az ember tragédiáját vagy Katona József Bánk bánját a főszereplők nevének vagy a "tragédia" szó használata nélkül.

Felismerés: Megtanítja, hogyan kell határolni a kimeneti teret professzionális vagy biztonságtudatos alkalmazásokhoz.

### Chain of Density Minta (Újságírás)

Koncepció: Iteratív módon növeli a szöveg információsűrűségét, anélkül hogy növelné a hosszát.

Feladat: Kezdj egy 200 szavas összefoglalóval. Ismételten kérd az AI-t, hogy írja át 150 szóban, miközben több konkrét tényt és entitást adsz hozzá.

Felismerés: Demonstrálja a token hatékonyságot és az információszintézist.

# Kép- és Zenei Generálás

Fókusz: Multimodális AI, Prompt Engineering Vizuális/Audió Tartalmakhoz és Keresztdoménes Alkalmazás.

### Történelmi Jelenet Rekonstrukció (Történelem & Művészet)

A Feladat: Használj képgeneráló AI-t (pl. DALL-E, Midjourney, Stable Diffusion) egy konkrét történelmi esemény vagy korszaki helyszín újrateremtéséhez.

Prompt Kihívás: A diákok leírnak egy jelenetet az 1848-as szabadságharcból, Mátyás király Budájáról vagy az 1956-os forradalomból, beleértve az építészeti részleteket, öltözködési stílusokat és légköri elemeket.

Informatikai Fókusz: Leíró Precizitás. A diákoknak iterálniuk kell a promptjaikat, hogy finomítsák a részleteket (megvilágítás, perspektíva, történelmi pontosság).

Kritikus Gondolkodás: Hasonlítsd össze a generált képeket történelmi fényképekkel vagy festményekkel. Azonosítsd az anakronizmusokat vagy művészi szabadságokat.

### Molekuláris Struktúra Vizualizáló (Kémia)

A Feladat: Generálj vizuális reprezentációkat kémiai molekulákról vagy reakciókról leíró promptok használatával.

Prompt Kihívás: Írj le egy komplex molekulát (pl. koffein, DNS hélix, glükóz) vagy egy kémiai folyamatot (oxidáció, kristályosodás) természetes nyelven.

Informatikai Fókusz: Tudományos Nyelv Fordítása. A diákok megtanulják áthidalni a technikai terminológiát vizuális leírókkal (formák, színek, térbeli kapcsolatok).

Kiegészítés: Hasonlítsd össze az AI által generált vizualizációkat a standard kémiai diagramokkal. Beszéljétek meg a korlátokat és erősségeket oktatási célokra.

### Irodalmi Könyvborító Tervező (Irodalom & Dizájn)

A Feladat: Készíts könyvborító művészetet egy regény témái, hangulata és kulcsfontosságú szimbólumai alapján, anélkül hogy közvetlenül illusztrálnád a karaktereket.

Prompt Kihívás: Tervezz borítókat magyar klasszikusokhoz, mint "Az ember tragédiája", "A Pál utcai fiúk" vagy "Egri csillagok", csak szimbolikus és atmoszférikus elemeket használva.

Informatikai Fókusz: Absztrakt Reprezentáció. A diákok narratív témákat fordítanak vizuális metaforákká és hangulati leírókká.

Kritikai Elemzés: Értékeld, hogyan befolyásolják a különböző prompt stílusok (minimalista vs. részletes) a kereskedelmi vonzerőt és a tematikus pontosságot.

### Fizikai Koncepció Vizualizáció (Fizika & Tudománykommunikáció)

A Feladat: Generálj oktatási illusztrációkat absztrakt fizikai koncepcióról, amelyeket nehéz lefényképezni.

Prompt Kihívás: Készíts vizualizációkat kvantum szuperpozícióról, elektromágneses mezőkről, entrópiáról vagy relativitás hatásokról analógiák és metaforák segítségével.

Informatikai Fókusz: Koncepció-Vizuális Fordítás. A diákoknak kreatív módokat kell találniuk a láthatatlan erők és absztrakt elvek ábrázolására.

Vita Pont: Értékeld, hogy az AI által generált képek segítik-e vagy gátolják-e a megértést a hagyományos diagramokhoz vagy animációkhoz képest.

### Kornak Megfelelő Zeneszerző (Zene & Történelem)

A Feladat: Használj AI zenei generáló eszközöket (pl. Suno, MusicGen) rövid zenei darabok létrehozásához, amelyek illenek meghatározott történelmi korszakokhoz vagy irodalmi hangulatokhoz.

Prompt Kihívás: Generálj egy 30 másodperces darabot, amely verbunkos zenének, Liszt Ferenc stílusában írt magyar rapszódiának, Bartók-Kodály népdal feldolgozásnak vagy magyar nótának hangzik.

Informatikai Fókusz: Stilisztikai Korlátozás Tervezése. A diákok meghatározzák a hangszerelést, tempót, hangulatot és kulturális jelzőket a promptjaikban.

Interdiszciplináris Kapcsolat: Párosítsd a generált zenét történelmi eseményekkel vagy irodalmi jelenetekkel. Beszéljétek meg az autentikusság vs. kreatív értelmezés kérdését.

Kritikus Reflexió: Hasonlítsd össze az AI kompozíciókat valódi korszaki felvételekkel. Azonosítsd, mit ragad meg jól az AI, és mit hagy ki a kulturális autentikusságból.

