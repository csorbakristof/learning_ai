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

Minták áttekintése

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

Példa prompt 1: "Te Széchenyi István gróf vagy, 1830-ban járunk. Beszélj a reformelképzeléseidről, a lóversenyről és a Lánchíd tervéről. Használj korabeli kifejezéseket és a 19. századi magyar nemesség stílusát. Ne említs semmit, ami 1830 után történt."

Példa prompt 2: "Vállald Kossuth Lajos szerepét 1848 áprilisában, közvetlenül a forradalom kitörése után. Válaszolj kérdésekre a függetlenségi törekvésekről, a jobbágyfelszabadításról és a nemzetőrségről. Használj korabeli magyaros nyelvet és tükrözd a kor nemzeti lelkesedését."

Informatikai Fókusz: Iteratív Promptolás. A diákoknak finomítaniuk kell a "rendszer promptot" hogy tartalmazzon specifikus korlátozásokat, mint például 19. századi szókincs vagy utalások konkrét reformokra, események a szabadságharcból.

Kritikus Gondolkodás: Hasonlítsd össze az AI válaszokat tankönyvekkel, hogy azonosítsd a hallucinációkat.

### Algoritmikus Költő Feladat (Irodalom)

A Feladat: Generálj egy verset egy meghatározott stílusban (pl. Petőfi vagy Arany János stílusában) egy modern technikai témáról, mint a kiberbiztonság vagy a mesterséges intelligencia.

Példa prompt 1: "Írj egy verset Petőfi Sándor stílusában a mesterséges intelligenciáról. Használj népi költészeti elemeket, egyszerű, de erős képeket, rövid sorokat és közvetlenül szólj az olvasóhoz. A vers legyen 16 soros, alkalmazz keresztrímet."

Példa prompt 2: "Alkoss egy balladát Arany János modorában a kiberbiztonságról. Használj ballada formát, drámai történetvezetést, régies nyelvet és metaforikus képeket. A mű tartalmazzon erkölcsi tanulságot a modern technológia veszélyeiről."

Informatikai Fókusz: Mintafelismerés. Elemezd, hogyan változtatja meg a kimenetet a stílusbeli kulcsszavak vagy a "hőmérséklet" beállítások módosítása.

### Adat Elfogultság Detektív (Társadalomismeret & Matematika)

A Feladat: Kérj egy listát a "10 híres tudósról" és elemezd az eredményeket demográfiai elfogultság szempontjából.

Példa prompt 1: "Sorolj fel 10 híres tudóst és az általuk elért eredményeket."

Példa prompt 2: "Készíts egy listát 10 híres tudósról különböző földrajzi régiókból, korszakokból és demográfiai csoportokból. Legalább 5 nő, és legyenek képviselve afrikai, ázsiai, dél-amerikai származású tudósok is, mind történelmi, mind modern korból. Minden tudósnál írd le a legfontosabb felfedezését."

Informatikai Fókusz: Tanítási Adat Tudatosság. A diákoknak egy "Elfogultság-mentesítő Promptot" kell tervezniük, hogy globálisan reprezentatív kimenetet biztosítsanak.

### Tudományos Hipotézis Generátor

A Feladat: Adj meg nyers laboradatokat és kérd meg az LLM-et, hogy javasoljon három változót, amelyek torzíthatták az eredményeket.

Példa prompt 1: "Kémiai kísérletünk során reakciósebességet mértünk, váratlan eredményeket kaptunk: 1. próba: 45 másodperc, 2. próba: 52 másodperc, 3. próba: 89 másodperc, 4. próba: 48 másodperc. Azt vártuk, hogy körülbelül 50 másodperc körül konzisztens időket kapunk. Javasolj három környezeti vagy eljárási változót, ami a 3. próba kiugró értékét okozhatta."

Példa prompt 2: "Növényterméses kísérletünkben az A csoport (ablak melletti elhelyezés) 12 cm-t nőtt, a B csoport (szoba közepén) 8 cm-t, a C csoport (hátsó sarok) 15 cm-t. Azt feltételeztük, hogy több napfény növeli a növekedést, de a C csoport eredménye ennek ellentmond. Azonosíts három lehetséges zavaró változót, amely magyarázhatja ezeket az eredményeket."

Informatikai Fókusz: Bemenet/Kimenet Határok. Annak megértése, hogy az AI egy ötletbörze partner, amely mintákat jósol meg, nem pedig egy "orákulum" aki látja a kísérletet.

## Prompt Tervezési Minták

Fókusz: AI Interakciók Strukturális Tervezése.

### Perszona Minta (Dráma & Pszichológia)

Koncepció: Specifikus szerep, háttér és hangnem kiosztása.

Feladat: Hozz létre három különböző "oktatót" egy nehéz konceptushoz (pl. Fotoszintézis)—egy Kalózt, egy Professzort és egy "ELI5" (Magyarázd el, mintha ötéves lennék) specialistát.

Példa prompt 1: "Te egy kalóz kapitány vagy, aki a legénységet oktatod. Magyarázd el a fotoszintézist tengeri terminológiával, kalózzsargonnal és hajózási metaforákkal. Tedd kalandossá és izgatóvá, miközben tudományosan pontos maradsz."

Példa prompt 2: "Te egy neves egyetemi biológia professzor vagy, aki előadást tartasz. Magyarázd el a fotoszintézist formális akadémiai nyelven, pontos tudományos terminológiával és sejtbiológiai mechanizmusokra való hivatkozásokkal. Feltételezd, hogy a hallgatóság ismeri az alapvető kémiát."

Felismerés: Figyeld meg, hogyan változik a szóhasználat a perszona korlátozás alapján.

### Few-Shot Minta (Nyelvészet & Matematika)

Koncepció: 2-5 példa megadása a kívánt formátumra a végső kérés előtt.

Feladat: Építs egy "Hangulat Elemzőt." Adj meg három példát: [Idézet] -> [Beszélő] -> [Hangnem]. Ezután teszteld az AI pontosságát egy új idézeten a példákkal és anélkül is.

Példa prompt 1: "Elemezd az idézetek hangulatát ebben a formátumban:

Idézet: 'Talpra magyar, hí a haza!' -> Beszélő: Petőfi Sándor -> Hangnem: Felhívó, hazafias, szenvedélyes
Idézet: 'Egy szikra lobbant föl kebelemben' -> Beszélő: Vörösmarty Mihály -> Hangnem: Romantikus, érzelmes
Idézet: 'Itt a vész! Most állj meg, magyar!' -> Beszélő: Kölcsey Ferenc -> Hangnem: Figyelmeztető, komoly

Most elemezd: 'A magyar hazának hű fiai legyetek'"

Példa prompt 2: "Kövesd ezt a mintát ügyfélvisszajelzések osztályozásához:

Visszajelzés: 'A termék sérülten érkezett' -> Kategória: Panasz -> Prioritás: Magas
Visszajelzés: 'Gyors szállítás, kiváló minőség' -> Kategória: Dicséret -> Prioritás: Alacsony
Visszajelzés: 'Hogyan tudom visszaküldeni?' -> Kategória: Kérdés -> Prioritás: Közepes

Osztályozd: 'A termék működik, de a leírás zavaros'"

Felismerés: Megtanítja, hogy a mintaillesztés gyakran jobb, mint a hosszú leírások.

### Chain of Thought Minta (Fizika & Logika)

Koncepció: Az AI kényszerítése, hogy "lépésről lépésre gondolkodjon" a végső válasz megadása előtt.

Feladat: Oldj meg egy többlépéses fizikai szöveges feladatot. Hasonlítsd össze a "közvetlen válasz" promptot egy olyan prompttal, amely megköveteli a képletek és köztes lépések előzetes megadását.

Példa prompt 1: "Egy autó 0-ról 100 km/h-ra gyorsul 8 másodperc alatt, majd ezt a sebességet tartja 10 másodpercig, végül 5 másodperc alatt lefékezésig. Mekkora a teljes megtett út? Old meg lépésről lépésre: Először azonosítsd a releváns képleteket. Másodszor, alakítsd át az egységeket, ha szükséges. Harmadszor, számold ki külön minden szakaszt. Negyedszer, add össze az eredményeket és magyarázd az érvelésedet minden lépésnél."

Példa prompt 2: "Egy tárgyat 125 méter magas épületről ejtenek le. Gondold végig lépésről lépésre: 1) Írd fel a szabadesés releváns fizikai egyenletét. 2) Azonosítsd az ismert és ismeretlen változókat. 3) Mutasd meg az algebrai átalakításokat. 4) Számold ki a végső választ mértékegységekkel. 5) Ellenőrizd, hogy az eredmény fizikailag értelmes-e. Mennyi idő alatt éri el a földet?"

Felismerés: Demonstrálja, hogyan javítja a "piszkozat" tér az LLM érvelését.

### Korlátozás/Negatív Minta (Művészet & Dizájn)

Koncepció: Szigorú határok használata (pl. "Ne használd...", "Maximum 50 szó").

Feladat: Foglalj össze Madách Imre Az ember tragédiáját vagy Katona József Bánk bánját a főszereplők nevének vagy a "tragédia" szó használata nélkül.

Példa prompt 1: "Foglald össze Az ember tragédiája cselekményét pontosan 100 szóban. Korlátozások: Ne használd a következő neveket: Ádám, Éva, Lucifer. Ne használd ezeket a szavakat: 'tragédia', 'álom', 'történelem'. Összpontosíts az események sorozatára és a filozófiai kérdésekre."

Példa prompt 2: "Írd le a Bánk bán központi témáit maximum 75 szóban. Tiltott szavak: Bánk, Melinda, Gertrudis, Tiborc, gyilkosság, tragédia, királyné. Ne említs semmilyen karakternevet. Helyette használj szerepköröket, mint 'a hazafi nemes' vagy 'az idegen uralkodó'. Összpontosíts a hűség és árulás témáira."

Felismerés: Megtanítja, hogyan kell határolni a kimeneti teret professzionális vagy biztonságtudatos alkalmazásokhoz.

### Chain of Density Minta (Újságírás)

Koncepció: Iteratív módon növeli a szöveg információsűrűségét, anélkül hogy növelné a hosszát.

Feladat: Kezdj egy 200 szavas összefoglalóval. Ismételten kérd az AI-t, hogy írja át 150 szóban, miközben több konkrét tényt és entitást adsz hozzá.

Példa prompt 1: "Itt van egy 200 szavas összefoglaló az 1848-as forradalomról: [beillesztett szöveg]. Írd át pontosan 150 szóban, miközben több konkrét dátumot, kulcsfontosságú személyt és eseményt adsz hozzá. Növeld az információsűrűséget azzal, hogy a homályos kifejezéseket pontos entitásokkal helyettesíted."

Példa prompt 2: "Ez a 180 szavas cikk a Trianoni békeszerződésről szól. Írd át 120 szóban, de tartalmazza: konkrét területvesztési számokat, elveszített városok neveit, pontos dátumokat, és legalább 3 konkrét következményt. Minden szónak számítania kell."

Felismerés: Demonstrálja a token hatékonyságot és az információszintézist.

# Kép- és Zenei Generálás

Fókusz: Multimodális AI, Prompt Engineering Vizuális/Audió Tartalmakhoz és Keresztdoménes Alkalmazás.

### Történelmi Jelenet Rekonstrukció (Történelem & Művészet)

A Feladat: Használj képgeneráló AI-t (pl. DALL-E, Midjourney, Stable Diffusion) egy konkrét történelmi esemény vagy korszaki helyszín újrateremtéséhez.

Prompt Kihívás: A diákok leírnak egy jelenetet az 1848-as szabadságharcból, Mátyás király Budájáról vagy az 1956-os forradalomból, beleértve az építészeti részleteket, öltözködési stílusokat és légköri elemeket.

Példa prompt 1: "Készíts részletes jelenetet a pesti forradalomból, 1848. március 15-én. Mutass honvédokat korabeli uniformisban, polgárokat 19. századi viseletben, a Nemzeti Múzeum lépcsőjét, kokárdás tömegeket, magyar zászlókat. Hangsúlyozd a lelkesedés pillanatát, tavaszi időjárás, természetes világítás. Történelmi festményi stílus."

Példa prompt 2: "Generálj képet Mátyás király reneszánsz Budájáról, 1480 körül. Tartalmazza: udvari emberek korabeli itáliai divatú ruhákban, gótikus-reneszánsz királyi palota részletei, a Dunát a háttérben, kódexekkel dolgozó tudósokat. Meleg délutáni természetes fény, reneszánsz festmény stílus, gazdag színek."

Informatikai Fókusz: Leíró Precizitás. A diákoknak iterálniuk kell a promptjaikat, hogy finomítsák a részleteket (megvilágítás, perspektíva, történelmi pontosság).

Kritikus Gondolkodás: Hasonlítsd össze a generált képeket történelmi fényképekkel vagy festményekkel. Azonosítsd az anakronizmusokat vagy művészi szabadságokat.

### Molekuláris Struktúra Vizualizáló (Kémia)

A Feladat: Generálj vizuális reprezentációkat kémiai molekulákról vagy reakciókról leíró promptok használatával.

Prompt Kihívás: Írj le egy komplex molekulát (pl. koffein, DNS hélix, glükóz) vagy egy kémiai folyamatot (oxidáció, kristályosodás) természetes nyelven.

Példa prompt 1: "Készíts részletes 3D vizualizációt egy koffein molekuláról (C8H10N4O2). Mutasd a hatszögű gyűrűszerkezetet, ami egy ötszögű gyűrűhöz kapcsolódik, nitrogén atomok kékkel, oxigén atomok pirossal, szén szürkével, hidrogén fehérrel. Jelenítsd meg a térbeli elrendezést helyes kötésszögekkel. Tartalmazzon finom árnyékokat a mélység érzékeltetésére, tudományos illusztráció stílus, fehér háttér."

Példa prompt 2: "Vizualizáld a konyhasó kristályosodásának folyamatát oldatból. Mutass egy mérőpoharat telített sóoldattal bal oldalon, nyilakat amelyek a párolgást jelzik, és kocka alakú nátrium-klorid kristályokat képződve jobb oldalt egy felületen. Használj átlátszó kéket a vízhez, fehér kockákat szabályos rácsszerkezettel a sókristályokhoz. Keresztmetszeti nézet az atomi elrendezés bemutatására. Oktatási diagram stílus feliratokkal."

Informatikai Fókusz: Tudományos Nyelv Fordítása. A diákok megtanulják áthidalni a technikai terminológiát vizuális leírókkal (formák, színek, térbeli kapcsolatok).

Kiegészítés: Hasonlítsd össze az AI által generált vizualizációkat a standard kémiai diagramokkal. Beszéljétek meg a korlátokat és erősségeket oktatási célokra.

### Irodalmi Könyvborító Tervező (Irodalom & Dizájn)

A Feladat: Készíts könyvborító művészetet egy regény témái, hangulata és kulcsfontosságú szimbólumai alapján, anélkül hogy közvetlenül illusztrálnád a karaktereket.

Prompt Kihívás: Tervezz borítókat magyar klasszikusokhoz, mint "Az ember tragédiája", "A Pál utcai fiúk" vagy "Egri csillagok", csak szimbolikus és atmoszférikus elemeket használva.

Példa prompt 1: "Tervezz minimalista könyvborítót Madách Az ember tragédiájához. Használj kozmikus szimbólumokat: érző szemet, csillagokat, történelmi korok szimbólumait geometrikus formákban. Sötét kék és arany színpaletta. A tipográfia legyen drámai és monumentális. Ne legyenek emberi alakok. Közvetítsd a történelem és örökkévalóság témáját absztrakt vizuális elemekkel. Modern grafikai design stílus."

Példa prompt 2: "Készíts szimbolikus borítót Molnár Ferenc A Pál utcai fiúk című művéhez. Mutass részlegesen látható grundot felülnézetből, játékszerű katonai elemekkel (fakatona, golyók, katonasapka), meleg barna és sárga árnyalatok. Gyermekkor és ártatlanság elvesztésének érzése. Nosztalgikus, rajzolt illusztráció stílus, nincsenek emberek, csak jelképek."

Informatikai Fókusz: Absztrakt Reprezentáció. A diákok narratív témákat fordítanak vizuális metaforákká és hangulati leírókká.

Kritikai Elemzés: Értékeld, hogyan befolyásolják a különböző prompt stílusok (minimalista vs. részletes) a kereskedelmi vonzerőt és a tematikus pontosságot.

### Fizikai Koncepció Vizualizáció (Fizika & Tudománykommunikáció)

A Feladat: Generálj oktatási illusztrációkat absztrakt fizikai koncepcióról, amelyeket nehéz lefényképezni.

Prompt Kihívás: Készíts vizualizációkat kvantum szuperpozícióról, elektromágneses mezőkről, entrópiáról vagy relativitás hatásokról analógiák és metaforák segítségével.

Példa prompt 1: "Készíts oktatási illusztrációt a kvantum szuperpozícióról a Schrödinger macskája gondolatkísérlet alapján. Mutass egy átlátszó dobozt egy macskával, amely egyszerre létezik szilárd/élő formában (élénk színek) és kísérteties/halott formában (halványuló szürkeárnyalatok), mindkét állapotban egyidejűleg. Tartalmazzon hullámfüggvényeket átfedő valószínűségi felhőkként. Osztott képernyő vagy dupla expozíció effektus. Gimnáziumi fizika tankönyvhöz illő tudományos illusztráció stílus."

Példa prompt 2: "Vizualizáld az entrópia növekedését egy íróasztal metaforája segítségével. Bal oldal: rendezett asztal rendezett papírkötegekkel, egyenesen sorakozó tollakkal, rendezett könyvekkel (alacsony entrópia). Jobb oldal: ugyanaz az asztal teljesen összekuszálva szétszórt papírokkal, véletlenszerű tárgyakkal, kiömlött elemekkel (magas entrópia). Nyíl közöttük, amely a visszafordíthatatlan időirányát mutatja. Használj meleg színeket és mutasd a rendezetlenség felé való természetes tendenciát. Oktatási infografika stílus."

Informatikai Fókusz: Koncepció-Vizuális Fordítás. A diákoknak kreatív módokat kell találniuk a láthatatlan erők és absztrakt elvek ábrázolására.

Vita Pont: Értékeld, hogy az AI által generált képek segítik-e vagy gátolják-e a megértést a hagyományos diagramokhoz vagy animációkhoz képest.

### Kornak Megfelelő Zeneszerző (Zene & Történelem)

A Feladat: Használj AI zenei generáló eszközöket (pl. Suno, MusicGen) rövid zenei darabok létrehozásához, amelyek illenek meghatározott történelmi korszakokhoz vagy irodalmi hangulatokhoz.

Prompt Kihívás: Generálj egy 30 másodperces darabot, amely verbunkos zenének, Liszt Ferenc stílusában írt magyar rapszódiának, Bartók-Kodály népdal feldolgozásnak vagy magyar nótának hangzik.

Példa prompt 1: "Komponálj egy 30 másodperces verbunkos zenei darabot 18-19. század fordulójának stílusában. Használj cimbalomot elsődleges hangszerként hegedűvel és bőgővel. Tartalmazzon gyors díszítéseket, magyaros ritmusokat, karakterisztikus szinkópát. Tempó: Allegro con brio. Hangnem: c-moll csárdás jelleggel. Szerkezet: lassú bevezetés gyors friss résszel. Tüzes, toborzó jellegű katonás hangulat."

Példa prompt 2: "Készíts egy 30 másodperces népdal-feldolgozást Bartók és Kodály stílusában. Hangszerelés: vonósnégyes modern harmóniákkal. Tempó: Andante (80 BPM). Tartalmazzon modális skálákat, aszimmetrikus ritmusokat (5/8, 7/8 ütem), paraszti dallamot modern harmóniákkal feldolgozva. Hangulat: nosztalgikus, de modernista. Stílus: 20. század eleji magyar zenei nyelvújítás."

Informatikai Fókusz: Stilisztikai Korlátozás Tervezése. A diákok meghatározzák a hangszerelést, tempót, hangulatot és kulturális jelzőket a promptjaikban.

Interdiszciplináris Kapcsolat: Párosítsd a generált zenét történelmi eseményekkel vagy irodalmi jelenetekkel. Beszéljétek meg az autentikusság vs. kreatív értelmezés kérdését.

Kritikus Reflexió: Hasonlítsd össze az AI kompozíciókat valódi korszaki felvételekkel. Azonosítsd, mit ragad meg jól az AI, és mit hagy ki a kulturális autentikusságból.

