# A feladat leírása

A feladatod a https://bmeaut.github.io/snippets/snippets/0216_VisitorObserverPelda/ oldalon található tananyagból egy HTML, JavaScript és Reveal.JS alapú prezentáció készítése, amit egyetemi hallgatóknak be lehet mutatni.

# Pontosítási kérdések és válaszok

1. **Célközönség szintje**: Milyen évfolyamos/féléves hallgatóknak szól a prezentáció? Van-e előzetes tudásuk a design patternekről?

Negyedéves, MSc hallgatók. Programozni tudnak és néhány egyszerűbb tervezési minta már szerepelt a tananyagban (Observer, Strategy, Facade).

2. **Prezentáció hossza**: Körülbelül hány perces előadáshoz kell a prezentáció? Hány diát képzelsz el?

A magyarázat a fontos, nem a hossza. Kb. 15 percre tervezem. Ha szép, forráskód centrikus a magyarázat animációkkal, akkor nem kell sok slide hozzá. De fedjük le a teljes anyagot.

3. **Nyelv**: Magyar vagy angol nyelvű legyen a prezentáció?

Magyar

4. **Reveal.JS téma**: Van-e preferált Reveal.JS téma (pl. black, white, league, sky, beige, simple, serif, night, moon, solarized)?

Legyen világos a háttér a projektor kontrasztja miatt. A "white" jó lesz.

5. **Kód példák megjelenítése**: Hogyan jelenjenek meg a kód példák? Syntax highlighting legyen? Teljes kód vagy csak részletek?

Legyen syntax highlighting. A kód már most is csak a lényeges részeket tartalmazza, így jó lenne minél többet mutatni belőle. Ha túl zsúfolt lenne a slide, akkor vágjunk belőle vagy használjunk valami görgethető animációt.

6. **Diagramok**: Az eredeti anyagban szereplő UML diagramokat és vizualizációkat hogyan jelenítsük meg? Átvegyük őket, vagy újrarajzoljuk (pl. Mermaid.js-sel)?

Nyugodtan újrarajzolhatod őket.

7. **Interaktivitás**: Legyenek-e interaktív elemek (pl. élő kód példák, animációk átmenetekkel) vagy statikus diák elegendőek?

Ha egy sima html fájlban meg lehet oldani, legyenek interaktív elemek is.

8. **Struktúra**: Hogyan strukturáljuk a tartalmat? Az eredeti anyag sorrendjét követve, vagy más felépítésben?

Kövesd az eddigi sorrendet.

9. **Gyakorlati feladatok/kvíz**: Kerüljön-e bele gyakorlati feladat vagy kvíz slide a végére az értés ellenőrzésére?

Igen, a test based learning elveire építve legyen a végén pár visszatekintő, ellenőrző kérdés.

10. **Speaker notes**: Kellenek-e előadói jegyzet (speaker notes) a diákhoz?

Speakter notes kevés kell. Csak hogy ne maradjon ki semmi fontos. Egyébként minden a fejemben van.

11. **Kiegészítő források**: Hivatkozzunk-e külső forrásokra, dokumentációkra a prezentációban?

Nem kell külső forrásra hivatkozni.

# Megvalósítás lépései

## 1. Projektstruktúra létrehozása
- Létrehozni a projekt mappát és a fő `index.html` fájlt
- Reveal.JS CDN-ről való betöltése (legújabb verzió)
- CSS fájlok beállítása: white téma, syntax highlighting (highlight.js vagy prism.js)
- Metadata beállítások: magyar nyelv, viewport, charset UTF-8

## 2. Prezentáció struktúrájának felépítése

### Slide-ok sorrendje (az eredeti anyag szerint):
1. **Címlap**: "Visitor és Observer minta" + rövid bevezetés
2. **Áttekintő slide**: Mit fogunk látni? (két design pattern együttes bemutatása)
3. **Ősosztályok - VisitorBase**: 
   - UML diagram (Mermaid.js)
   - Forráskód syntax highlightinggal
   - Magyarázat: visitor minta alapelve
4. **Ősosztályok - ObserverBase**:
   - UML diagram
   - Forráskód
   - Magyarázat: observer minta alapelve
5. **Ősosztályok - ElementBase**:
   - UML diagram
   - Forráskód (observers vektor, metódusok)
   - Magyarázat: közös elem ősosztály
6. **Element osztályok - ElementInt**:
   - Forráskód részletes
   - Kiemelés: Accept metódus (visitor) és SetValue (observer értesítés)
7. **Element osztályok - ElementString**:
   - Forráskód részletes
   - Hasonlóságok kiemeléséhez animáció
8. **Konkrét Visitor implementáció**:
   - Forráskód
   - Magyarázat: +100 művelet minden elemre
   - Visitor előnyei (új művelet új osztály módosítás nélkül)
9. **Konkrét Observer implementáció**:
   - Forráskód
   - Kiírás console-ra változásokról
10. **ElementContainer osztály**:
    - Forráskód
    - Smart pointerek (unique_ptr) magyarázata
    - Move semantics említése
11. **Főprogram - elemek létrehozása**:
    - Forráskód részlet: elemek létrehozása, observer regisztráció
    - Move semantics újrahasznosítás
12. **Főprogram - működés**:
    - Teljes futási kimenet
    - Lépésről lépésre: Before visit → During visit → After visit
    - Animáció: hogyan változnak az értékek
13. **Teljes UML diagram**:
    - Összes osztály kapcsolata Mermaid.js-sel
    - Átfogó kép a rendszerről
14. **Összefoglalás**:
    - Visitor minta: új művelet hozzáadása meglévő osztályokhoz
    - Observer minta: értesítési mechanizmus
    - Együttes alkalmazás előnyei
15. **Ellenőrző kérdések** (test-based learning):
    - 3-5 visszatekintő kérdés kvíz formában
    - Pl.: "Mi a Visitor Accept metódusának szerepe?"
    - Pl.: "Mikor értesülnek az observerek?"
    - Pl.: "Miért használunk unique_ptr-t?"

## 3. Forráskód megjelenítés implementálása
- Syntax highlighting beállítása C++ kódhoz
- Minden kód slide-nél:
  - Használjunk `<pre><code class="cpp">` tageket
  - Opcionálisan: görgethető div, ha túl hosszú (`max-height` + `overflow-y: scroll`)
- Kód animációk:
  - Reveal.js fragment-ek használata kód részletek fokozatos megjelenítéséhez
  - Kiemelések (highlight) fontos sorokra

## 4. UML diagramok készítése Mermaid.js-sel
- Beágyazni a Mermaid.js library-t
- Létrehozni az osztálydiagramokat:
  - VisitorBase interfész
  - ObserverBase interfész
  - ElementBase ősosztály és leszármazottjai
  - Visitor és Observer konkrét osztályok
  - ElementContainer
  - Kapcsolatok: öröklődés, aggregáció, függőség
- Teljes rendszer diagram külön slide-on

## 5. Interaktív elemek hozzáadása
- **Futási kimenet animáció**: A főprogramnál animálni a kimenet megjelenését step-by-step
- **Kód highlight animáció**: Fragment-ekkel kiemeijük, hogy melyik sor mit csinál
- **Kérdés-válasz kártyák**: A végső ellenőrző kérdéseknél kattintásra megjelenő válaszok
- **Navigáció**: Reveal.js alapértelmezett navigáció (nyilak + progress bar)

## 6. Speaker notes hozzáadása
- Minimal notes minden slide-hoz az `<aside class="notes">` tag-ben:
  - Főbb pontok, amiket mindenképpen érinteni kell
  - Példák, amikre utalni lehet
  - Időzítési jelzések (ha szükséges)
- Különösen fontos slide-ok: Visitor accept működése, observer értesítés mechanizmus

## 7. Styling és formázás finomítása
- White téma alkalmazása
- Font-ok: jól olvasható, kontrasztos
- Kód blokkok: megfelelő méret, ne legyen túl kicsi projektor esetén
- Slide-ok ne legyenek túlzsúfoltak
- Padding, margin optimalizálás
- Responsive design (különböző képernyőméretekre)

## 8. Ellenőrző kérdések kidolgozása
Példa kérdések (test-based learning):
1. **Mi a Visitor minta fő előnye?**
   - Új művelet hozzáadása meglévő osztályok módosítása nélkül
2. **Hogyan értesülnek az observerek az értékváltozásról?**
   - A SetValue metódus végigmegy az observers vektoron
3. **Miért fontos az Accept metódusban a visitor visszahívása?**
   - Így automatikusan a megfelelő típusú Visit metódus hívódik (double dispatch)
4. **Mit csinál a unique_ptr move semantika?**
   - Átadja az ownership-et, az eredeti pointer nullptr lesz
5. **Milyen előnye van a két minta együttes alkalmazásának?**
   - Visitor új műveleteket ad, Observer pedig értesít a változásokról

## 9. Tesztelés és finomhangolás
- Prezentáció megnyitása böngészőben
- Tesztelés:
  - Minden slide megjelenik-e helyesen
  - Animációk működnek-e
  - Syntax highlighting helyes-e
  - Mermaid diagramok renderelődnek-e
  - Kérdések interakciója működik-e
  - Speaker notes láthatók-e (S billentyű)
- Navigáció: előre-hátra lépés, overview mode (ESC)
- Különböző böngészőkben tesztelés (Chrome, Firefox, Edge)
- Projektoros megjelenítés szimulálása (kontrasztosság, olvashatóság)

## 10. Dokumentáció és használati útmutató
- README.md fájl a prezentációhoz:
  - Hogyan kell megnyitni (böngészőben)
  - Navigációs billentyűk (nyilak, Space, S = speaker notes, ESC = overview)
  - Külső függőségek (CDN linkek)
  - Időtartam: ~15 perc
- Opcionálisan: PDF export lehetőség dokumentálása
