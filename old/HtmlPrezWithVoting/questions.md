Feleletválasztós kérdésbank
1. kategória: Fájlrendszer és tárolási mechanizmusok
C1Q1: Mi történik a fájlok fizikai bitjeivel a merevlemezen, amikor "törlöd" őket a lomtárból?
A) Minden bit azonnal felülíródik véletlenszerű 1-esekkel és 0-kkal.
B*) A bitek megmaradnak, de a fájlrendszer szabadnak jelöli a helyet az új adatok számára.
C) A hardver fizikailag lemágnesezi a lemez adott szektorait a törléshez.
D) Nem tudom.
C1Q2: Mi az elsődleges különbség az abszolút elérési út és a szimbolikus link (parancsikon) között?
A*) Az abszolút út a tényleges lemezcím; a szimbolikus link egy apró fájl, ami erre a címre mutat.
B) Az abszolút út a fájl másolata; a szimbolikus link az eredeti fájl.
C) Az OS szempontjából teljesen azonos módon kezelődnek.
D) Nem tudom.
C1Q3: Miért fejeződik be a USB meghajtó "Gyorsformázása" másodpercek alatt, míg a "Teljes formázás" sokáig tart?
A) A teljes formázás titkosítja a meghajtót, a gyorsformázás nem.
B) A gyorsformázás csak a mappákat törli, a fájlokat nem.
C*) A gyorsformázás csak a "Tartalomjegyzéket" (FAT/MFT) törli; a teljes formázás minden szektort ellenőriz.
D) Nem tudom.
C1Q4: Ha átnevezel egy fájlt notes.txt-ről notes.exe-re, mi történik a fájl belső adatszerkezetével?
A*) Semmi nem történik az adatokkal; csak a címke (kiterjesztés) változik meg, amit az OS a program kiválasztásához használ.
B) Az OS automatikusan átalakítja a szöveget gépi kódú utasításokká.
C) A fájl megsérül, mert a bitek újrarendeződnek.
D) Nem tudom.
2. kategória: Operációs rendszer és folyamatkezelés
C2Q1: Az OS melyik komponense felelős a hardver közvetlen kezeléséért és fut védett, kiváltságos módban?
A) A felhasználói módú Shell.
B) A Rendszerleíró adatbázis (Registry).
C*) A Kernel (rendszermag).
D) Nem tudom.
C2Q2: Hogyan képes egy egymagos CPU látszólag több alkalmazást futtatni egyszerre?
A*) "Kontextusváltás" (Context Switching) használatával, ami gyorsan cserélgeti a CPU-t használó folyamatokat.
B) A CPU mag virtuális al-magokra bontásával minden app számára.
C) Az összes app egyidejű futtatásával egy közös memóriaterületen.
D) Nem tudom.
C2Q3: Mi a célja a PATH környezeti változónak a shellben?
A*) Megad egy listát azokról a könyvtárakról, ahol az OS-nek keresnie kell a futtatható programokat.
B) Eltárolja a felhasználó által beírt összes parancs előzményeit.
C) Meghatározza a terminál ablak vizuális témáját és színeit.
D) Nem tudom.
C2Q4: Mik azok a stdout és stderr egy futó folyamat kontextusában?
A) Két rejtett mappa, ahol az OS az ideiglenes alkalmazásadatokat tárolja.
B*) Két szabványos szöveges folyam: egy a normál kimenetnek, egy pedig a hibaüzeneteknek.
C) Minden C# konzolalkalmazás két fő szálának neve.
D) Nem tudom.
C2Q5: Az alábbiak közül melyik írja le legjobban a "Bootloader"-t?
A*) Egy apró kódrészlet, amely megkeresi és betölti a fő OS Kernelt a memóriába.
B) Egy program, amely frissítéseket tölt le az internetről az OS indulása előtt.
C) A BIOS azon része, amely lehetővé teszi a rendszeróra átállítását.
D) Nem tudom.
3. kategória: Hardver-szoftver interfész
C3Q1: A memóriahierarchiában melyik tároló található fizikailag a CPU-n belül, és nyújtja a legnagyobb sebességet?
A*) Regiszterek.
B) L3 Cache.
C) RAM (Random Access Memory).
D) Nem tudom.
C3Q2: Mire utal az "x64" kifejezés a CPU architektúrák kapcsán?
A) Az egyszerre futtatható programok maximális számára.
B) A processzor maximális órajelére Gigahertzben.
C*) A CPU regisztereinek szélességére és az általa kezelt memóriacímek méretére.
D) Nem tudom.
C3Q3: Az alábbiak közül melyik állítás igaz a "Veremre" (Stack) és a "Kupacra" (Heap)?
A) A Vermet nagy fájlok tárolására, a Kupacot kis számokra használják.
B) A C# minden változót a Vermen tárol a nagy teljesítmény érdekében.
C*) A Verem gyors és a lokális változókat kezeli; a Kupac rugalmas és a hosszú életű objektumokat kezeli.
D) Nem tudom.
C3Q4: Mi az a "Rendszerhívás" (syscall)?
A*) Egy alkalmazás kérése a Kernel felé egy hardverszintű feladat elvégzésére.
B) Egy telefonhívás az IT részleg felé egy szerverhiba javítására.
C) Egy hibaüzenet, ami akkor keletkezik, ha a CPU túlmelegszik.
D) Nem tudom.
4. kategória: Hálózati alapok
C4Q1: Mit jelent a 127.0.0.1 IP-cím (localhost)?
A) A legközelebbi DNS szerver címe.
B*) Egy loopback cím, amely magára a lokális gépre utal.
C) A helyi Wi-Fi hálózat alapértelmezett átjárója (gateway).
D) Nem tudom.
C4Q2: Mi a "Port" szerepe a hálózatkezelésben?
A) Meghatározza az internetre való csatlakozáshoz használt fizikai kábelt.
B) Meghatározza az adatátvitel maximális sebességét.
C*) Al-címként szolgál a forgalom irányításához egy adott gépen futó alkalmazáshoz.
D) Nem tudom.
C4Q3: Mi a DNS (Domain Name System) szerver elsődleges feladata?
A*) Az ember által olvasható nevek (pl. bme.hu) lefordítása IP-címekre.
B) A weboldalak fájljainak tárolása (pl. google.com).
C) A helyi hálózat védelme az illetéktelen hackerektől.
D) Nem tudom.
5. kategória: Build és Runtime folyamat
C5Q1: Mi a transzformációs sorrend egy C# programnál a forráskódtól a végrehajtásig?
A) Forráskód -> Gépi kód -> IL.
B) Forráskód -> Assembly -> Java Bytecode.
C*) Forráskód -> IL (CIL) -> Gépi kód (JIT-en keresztül).
D) Nem tudom.
C5Q2: Mi történik egy DLL "Dinamikus linkelése" során?
A) A könyvtár kódja fizikailag beleírodik az .exe fájlba a fordítás során.
B) A könyvtár letöltődik az internetről minden alkalommal, amikor az app fut.
C*) A könyvtár kódja csak akkor töltődik be a memóriába, amikor az alkalmazás elindul vagy szüksége van rá.
D) Nem tudom.
C5Q3: Miért kezeli jobban az UTF-8 kódolású fájl az emojikat, mint az ASCII kódolású?
A*) Az UTF-8 több bájtot használ több ezer karakter ábrázolásához; az ASCII 128-ra van korlátozva.
B) Az UTF-8 gyorsabb tömörítési algoritmust használ.
C) Az ASCII-t csak számokhoz tervezték, míg az UTF-8-at művészeti célokra.
D) Nem tudom.
6. kategória: Git és verziókezelési mechanizmusok
C6Q1: Ha letörlöd a rejtett .git mappát a projektedben, mi történik a korábbi commit-jaiddal?
A) Biztonságban vannak a felhőben (GitHub), és automatikusan újra megjelennek.
B*) Végleg elvesznek a lokális gépedről a teljes verziótörténettel együtt.
C) Áthelyeződnek a rendszer ideiglenes "visszavonási" pufferrébe 30 napra.
D) Nem tudom.
C6Q2: Mi az a Git "Commit Hash" (pl. a1b2c3d...)?
A) Egy véletlenszerű jelszó, amit a fejlesztőhöz rendeltek.
B*) Egy egyedi azonosító, amely a fájlok pontos állapotából generálódik abban a commitban.
C) A fejlesztő e-mail címének titkosított változata.
D) Nem tudom.
C6Q3: Hogyan tárolja a Git belsőleg a változásokat?
A) Minden egyes commit-hoz eltárolja minden egyes fájl teljes másolatát.
B) A fájlokat titkosított ZIP archívumként menti a Windows Registry-be.
C*) Elsősorban "snapshot"-okat (pillanatképeket) tárol, és tömörítést/deltákat használ a helytakarékossághoz.
D) Nem tudom.
C6Q4: Mi a "Branch" (ág) a Git-ben?
A*) Egy könnyűsúlyú mutató egy adott commit-ra.
B) A teljes projekt egy teljes másolati mappája.
C) Egy külön felhasználói fiók a GitHub weboldalán.
D) Nem tudom.
C6Q5: Mit jelentenek az olyan jelölők a fájlban, mint a <<<<<<< HEAD?
A) Speciális komment típus dokumentációs célokra.
B*) Egy Merge Conflict-ot (összefűzési konfliktus), amit a fejlesztőnek manuálisan kell feloldania.
C) Egy parancs, ami arra utasítja a fordítót, hogy ugorjon át egy kódblokkot.
D) Nem tudom.
C6Q6: Mi a fő különbség a Git és a GitHub között?
A) A Git a Windows-hoz van; a GitHub a Mac/Linux-hoz.
B) A GitHub a Git szoftver legújabb verziója.
C*) A Git a lokális verziókezelő eszköz; a GitHub egy felhőplatform a repozitóriumok hosztolásához.
D) Nem tudom.
7. kategória: Memóriakezelés és objektum életciklus
C7Q1: Egy 64 bites rendszeren mennyi memóriát foglal egy C# referencia (mutató)?
A*) 8 bájt.
B) 4 bájt.
C) Változó, az osztály méretétől függően.
D) Nem tudom.
C7Q2: Mikor szabadítja fel a C# Garbage Collector (GC) egy objektum által használt memóriát?
A) Azonnal, amint a változó kikerül a hatókörből (scope).
B) Csak akkor, ha a felhasználó manuálisan meghívja az Object.Dispose()-t.
C*) Egy későbbi időpontban, amit a GC belső heurisztikái és a memórianyomás határoz meg.
D) Nem tudom.
C7Q3: Mi a new kulcsszó "költsége" C#-ban?
A*) Megköveteli a runtime-tól, hogy találjon és lefoglaljon egy összefüggő területet a Kupacban.
B) 1 centbe kerül felhő alapú licencdíjként.
C) Arra kényszeríti a CPU-t, hogy indítsa újra a szálat a memóriaszivárgások megelőzése érdekében.
D) Nem tudom.
C7Q4: Mi a NullReferenceException a hardver szintjén?
A) A RAM chip válaszadási hibája egy kérésre.
B*) A CPU megpróbál olvasni egy olyan memóriacímről, ami valójában nulla (0x0).
C) Hiba, ahol a fejlesztő elfelejtett nevet adni egy változónak.
D) Nem tudom.
C7Q5: Mi történik az objA = objB utasítás végrehajtásakor két osztálypéldány esetén C#-ban?
A) Az objB-ben lévő adatok átmásolódnak az objA memóriahelyére.
B) A két objektum egyetlen nagyobb objektummá vonódik össze.
C*) Az objB által tartott memóriacím (referencia) másolódik át az objA-ba.
D) Nem tudom.
8. kategória: Szálkezelés és az Event Loop
C8Q1: Miért okozza egy hosszú számítás a UI szálon az ablak "Nem válaszol" állapotát?
A*) A szál elakadt a ciklusban, és nem tudja feldolgozni a sorban álló "Paint" vagy "Click" eseményeket.
B) Az OS azt hiszi, hogy az app halott, és lekapcsolja az áramellátását.
C) A RAM túlságosan felforrósodik a nagy sebességű számítástól.
D) Nem tudom.
C8Q2: Mi az "overhead" (többletköltség) egy fizikai Szál (Thread) létrehozásakor egy Task-hoz képest?
A) A Szál valójában olcsóbb, mint a Task, mert "natív".
B*) A Szál jelentős memóriát (pl. 1MB stack) és OS szintű kezelést igényel.
C) Nincs különbség; csak két különböző név ugyanarra a dologra.
D) Nem tudom.
C8Q3: Mi az a "Race Condition"?
A) Verseny a fejlesztők között egy funkció leggyorsabb befejezéséért.
B) Amikor egy program gyorsabban fut, mint amit a hálózat kezelni tud.
C*) Amikor a végeredmény több szál kiszámíthatatlan időzítésétől függ.
D) Nem tudom.
C8Q4: Mi történik Holtpont (Deadlock) esetén?
A*) Két vagy több szál örökre elakad, mindegyik olyan erőforrásra várva, amit a másik tart fogva.
B) A számítógép merevlemeze megáll.
C) Az alkalmazás befejezi a munkáját és megfelelően leáll.
D) Nem tudom.
C8Q5: Az await kulcsszó C#-ban minden esetben létrehoz egy új fizikai szálat?
A*) Nem; gyakran csak "átadja" (yield) a jelenlegi szálat, amíg a munka be nem fejeződik.
B) Igen, ez az aszinkron programozás definíciója.
C) Csak akkor, ha a számítógépnek több mint 4 CPU magja van.
D) Nem tudom.
9. kategória: Adatábrázolás és szerializáció
C9Q1: Mit ír le az "Endianness" (Little Endian vs. Big Endian)?
A) A fájlok sorrendjét egy mappában.
B) Azt, hogy egy program a fájl elején vagy végén kezdődik.
C*) A bájtok sorrendjét, ahogyan egy többájtos érték eltárolódik a memóriában.
D) Nem tudom.
C9Q2: Miért tudod elolvasni az XML fájlt Notepadben, de egy képfájl "halandzsának" tűnik?
A*) Az XML szövegként (kódolt karakterek) tárolódik; a képek nyers bináris adatként.
B) Az XML fájlok kisebbek, mint a képfájlok.
C) A Notepad csak a Microsoft által készített fájlokat támogatja.
D) Nem tudom.
C9Q3: Miért kell "escape"-elni a karaktereket, mint pl. a < jelet XML-ben vagy a " jelet egy C# stringben?
A*) Mert ezeknek a karaktereknek speciális jelentése van a parser/fordító számára.
B) Mert ezek a karakterek illegálisak a modern operációs rendszerekben.
C) Hogy a kódot nehezebb legyen elolvasni a hackerek számára.
D) Nem tudom.
C9Q4: Miért nem egyenlő gyakran a 0.1 + 0.2 a 0.3-mal C# double változók esetén?
A) A számítógép rossz az alapvető összeadásban.
B) A + operátor a legközelebbi egész számra kerekít.
C*) A 2-es alapú bináris lebegőpontos ábrázolás nem tud pontosan reprezentálni néhány tizedestörtet.
D) Nem tudom.
C9Q5: Mi az a "Buffer Overflow"?
A*) Amikor az adatokat a lefoglalt memóriapuffer határán túlra írják.
B) Amikor az internetkapcsolat gyorsabb, mint amit a számítógép kezelni tud.
C) Amikor egy mappa több mint 1000 fájlt tartalmaz.
D) Nem tudom.
10. kategória: Menedzselt futtatókörnyezet
C10Q1: Mi az az "Unmanaged Code" (nem menedzselt kód) a .NET kontextusában?
A) Projektmenedzser nélkül írt kód.
B*) Olyan kód (mint a C++ vagy assembly), amely közvetlenül az OS-en fut GC vagy biztonsági ellenőrzések nélkül.
C) Olyan kód, amelyet a Microsoft "elavultnak" (deprecated) jelölt.
D) Nem tudom.
C10Q2: Mi az Intermediate Language (IL) elsődleges előnye?
A*) Lehetővé teszi, hogy ugyanaz a lefordított kód bármilyen platformon fusson, ahol van kompatibilis runtime.
B) Gyorsabbá teszi a programot a natív kódhoz képest.
C) Megakadályozza, hogy a forráskódot ellopják más fejlesztők.
D) Nem tudom.
C10Q3: Miért lassabb néha egy .NET app legelső alkalommal, amikor egy függvényt meghívunk?
A) A számítógép éppen "felébreszti" a merevlemezt.
B*) A JIT fordító éppen lefordítja az IL-t gépi kódra az adott függvényhez.
C) Az OS éppen ellenőrzi a felhasználó licenckulcsát.
D) Nem tudom.
C10Q4: Mi az a "Reflekció" (Reflection) C#-ban?
A) A képesség, hogy látod az arcodat a laptop képernyőjén.
B*) Egy program képessége, hogy futásidőben vizsgálja a saját metaadatait, típusait és metódusait.
C) Egy technika a képek vízszintes tükrözésére a UI-ban.
D) Nem tudom.
C10Q5: Mi volt a Global Assembly Cache (GAC) célja?
A*) Központi DLL-ek megosztása sok különböző alkalmazás között egy gépen.
B) Az egész C: meghajtó biztonsági mentésének tárolása.
C) Nagy sebességű gyorsítótárként szolgált a böngésző képeihez.
D) Nem tudom.
11. kategória: Archívumok, tömörítés és terminál ismeretek
C11Q1: Miért nem lehet általában egy összetett .NET appot közvetlenül egy ZIP-ből futtatni kicsomagolás nélkül?
A) A ZIP fájlok alapértelmezés szerint titkosítottak.
B) A Windows tiltja a .zip végződésű fájlok futtatását.
C*) Az app nem találja a függőségeit (DLL-ek), vagy nem tud lokális konfigurációs fájlokat írni.
D) Nem tudom.
12. kategória: Shell-ek, Kernelek és Userland
C12Q1: Miben különbözik alapvetően a PowerShell a régi CMD-től?
A*) A PowerShell "Objektumokat" ad át a parancsok között; a CMD "Stringeket" (szöveget).
B) A PowerShell-nek kék háttere van fekete helyett.
C) A PowerShell csak szervereken érhető el.
D) Nem tudom.
C12Q2: A terminál ablak (cmd.exe) része az operációs rendszer Kernelének?
A) Igen, ez az OS legalacsonyabb szintje.
B) Attól függ, hogy Administrator-ként futtatod-e.
C*) Nem; ez csak egy rendes alkalmazás, ami a "Userland"-ben (felhasználói módban) fut.
D) Nem tudom.
C12Q3: Mi az a "Szolgáltatás" (Service vagy Daemon) a számítógépen?
A) Egy személy, aki kijön megjavítani a hardvert.
B*) Egy program, amely a háttérben fut felhasználói felület nélkül.
C) Egy speciális típusú nagy sebességű internetkapcsolat.
D) Nem tudom.
C12Q4: Hogyan "indít el" a Shell egy programot, amikor beírod a nevét?
A) Átmásolja a program kódját a saját memóriaterületére.
B) Üzenetet küld a BIOS-nak a CPU újraindítására.
C*) Rendszerhívást (system call) intéz a Kernel felé egy új folyamat (Process) létrehozására.
D) Nem tudom.
C12Q5: Miért nem tud egy "Felhasználói alkalmazás" beleolvasni egy másik futó alkalmazás memóriájába?
A*) Az OS Kernel minden folyamatnak saját, izolált virtuális címtartományt ad a biztonság érdekében.
B) Mert a memória minden app számára titkosított.
C) Nincs elég hely a buszon, hogy két app egyszerre beszélgessen.
D) Nem tudom.
13. kategória: Eszközláncok és Deployment
C13Q1: Miért bukik el gyakran, ha csak az .exe fájlt másolod át a Debug mappádból egy másik PC-re?
A) Mert az .exe fájl a te konkrét CPU-dhoz van kötve.
B*) Hiányoznak a szükséges DLL-ek és konfigurációs fájlok (függőségek).
C) A Visual Studio "próbaidőszakot" ad minden debug build-hez.
D) Nem tudom.
C13Q2: Mi a különbség a statikus könyvtár (.lib) és a dinamikus könyvtár (.dll) között?
A) A statikus könyvtárak a C++ hoz vannak; a dinamikusak a C#-hoz.
B) A dinamikus könyvtárak gyorsabbak, de több helyet foglalnak a lemezen.
C*) A statikus könyvtárak beépülnek az exe-be; a dinamikusak külön fájlok maradnak.
D) Nem tudom.
C13Q3: Hogyan találja meg a Windows OS az appodnak szükséges DLL-eket futásidőben?
A*) Ellenőrzi a konkrét helyeket: az app mappáját, a PATH-t és a rendszermappákat.
B) Átkutatja a teljes merevlemezt, amíg meg nem találja őket.
C) Megkéri a felhasználót, hogy mutasson rá a mappára minden app induláskor.
D) Nem tudom.
C13Q4: Mi az a .csproj fájl egy .NET projektben?
A) Az összes forráskód tömörített változata.
B*) Egy XML fájl, amely utasításokat tartalmaz a build motor (MSBuild) számára.
C) A tényleges bináris fájl, ami a felhasználó gépén fut.
D) Nem tudom.
C13Q5: Mi a fő hátránya a "Framework-Dependent" (keretrendszer-függő) publikálásnak?
A*) A célgépen telepítve KELL lennie a .NET Runtime megfelelő verziójának.
B) A végeredmény fájlmérete rendkívül nagy lesz.
C) Nem futhat más gépen, csak a fejlesztőén.
D) Nem tudom.
