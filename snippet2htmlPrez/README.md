# Visitor és Observer Minta - Prezentáció

Interaktív HTML prezentáció a Visitor és Observer tervezési minták bemutatására, Reveal.js alapokon.

## Tartalom

A prezentáció a https://bmeaut.github.io/snippets/snippets/0216_VisitorObserverPelda/ oldalon található tananyag alapján készült.

**Témák:**
- Visitor design pattern
- Observer design pattern
- C++ implementáció példákkal
- Smart pointerek (unique_ptr, move semantics)
- UML diagramok
- Interaktív kód példák
- Ellenőrző kérdések

## Használat

### Megnyitás

1. Nyisd meg az `index.html` fájlt egy modern böngészőben (Chrome, Firefox, Edge)
2. A prezentáció automatikusan betöltődik

**Vagy egyszerűen:** Dupla klikk az `index.html` fájlon

### Navigáció

**Billentyűparancsok:**
- `→` / `Space` - Következő slide
- `←` - Előző slide
- `↓` / `↑` - Vertikális navigáció (ha van)
- `Home` - Első slide
- `End` - Utolsó slide
- `ESC` - Overview mode (összes slide áttekintése)
- `S` - Speaker notes megjelenítése (előadói jegyzetek)
- `F` - Fullscreen mode
- `?` - Súgó (összes billentyűparancs)

**Egér/Érintés:**
- Kattintás a slide jobb/bal szélén: előre/hátra
- Swipe: mobilon jobbra/balra csúsztatás

### Funkciók

- **Syntax Highlighting**: C++ kód automatikus színezése
- **Fragmentek**: Fokozatos megjelenítés (kattintással/Space-szel)
- **UML Diagramok**: Mermaid.js-sel generált osztálydiagramok
- **Interaktív kérdések**: Ellenőrző kérdések kattintható válaszokkal
- **Speaker Notes**: Előadói jegyzetek minden slide-hoz (S billentyűvel)
- **Animációk**: Kód kiemelések, output megjelenítés lépésenként

### Speaker Mode

1. Nyomd meg az `S` billentyűt
2. Megnyílik egy új ablak az előadói nézettel:
   - Aktuális slide
   - Következő slide előnézet
   - Speaker notes
   - Időzítő
3. Az eredeti ablakon mutasd a prezentációt, a speaker view-t csak te látod

## Prezentáció Struktúra

**Összesen:** ~21 slide
**Időtartam:** ~15 perc
**Nyelv:** Magyar

### Slide-ok:
1. Címlap
2. Áttekintés
3. VisitorBase ősosztály
4. ObserverBase ősosztály
5. ElementBase ősosztály
6. ElementInt osztály
7. ElementString osztály
8. Konkrét Visitor
9. Konkrét Observer
10. ElementContainer
11. Smart Pointerek részletek
12. Főprogram - létrehozás
13. Főprogram - működés
14. Teljes UML diagram
15. Összefoglalás
16-21. Ellenőrző kérdések (5 db + intro)
22. Köszönöm slide

## Technikai részletek

### Külső függőségek (CDN-ről töltődnek):
- **Reveal.js 4.5.0** - Prezentációs keretrendszer
- **Highlight.js** - Syntax highlighting
- **Mermaid.js 10.x** - UML diagram renderelés

### Böngésző követelmények:
- Modern böngésző (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+)
- JavaScript engedélyezve
- Internetkapcsolat (CDN tartalmak betöltéséhez)

### Offline használat:
Ha offline szeretnéd használni, töltsd le a Reveal.js, Highlight.js és Mermaid.js fájlokat, és módosítsd az index.html-ben a CDN linkeket lokális útvonalakra.

## PDF Export

Reveal.js támogatja a PDF exportot:

1. Nyisd meg a prezentációt Chrome-ban
2. Add hozzá az URL végéhez: `?print-pdf`
   - Példa: `file:///e:/_learning_ai/snippet2htmlPrez/index.html?print-pdf`
3. Nyomtasd PDF-be (Ctrl+P → Mentés PDF-ként)

**Beállítások:**
- Layout: Landscape (fekvő)
- Margins: None
- Background graphics: Yes

## Testreszabás

Az `index.html` fájl `<style>` szekciójában módosíthatod:
- Színsémát
- Font méreteket
- Slide átmeneteket
- Kód blokk magasságokat

A Reveal.js inicializálásban (`Reveal.initialize`) állíthatod:
- Átmenet típusát (`transition`)
- Slide méretét (`width`, `height`)
- Auto-slide időzítést

## Hibakeresés

**Mermaid diagramok nem jelennek meg:**
- Ellenőrizd az internetkapcsolatot
- Nézd meg a böngésző konzolt (F12) hibaüzenetekért
- Néhány diagram betöltés lassabb lehet első alkalommal

**Syntax highlighting nem működik:**
- Várj pár másodpercet a betöltésre
- Frissítsd az oldalt (Ctrl+R)

**Speaker notes nem látszanak:**
- Nyomd meg az `S` billentyűt
- Engedélyezd a popup ablakokat a böngészőben

## Forrás

Eredeti tananyag: https://bmeaut.github.io/snippets/snippets/0216_VisitorObserverPelda/

Forráskód: https://github.com/csorbakristof/alkalmazasfejlesztes/tree/master/VisitorObserverPelda

## Licenc

Az eredeti tananyag BME AUT tulajdona.
A prezentáció oktatási célra szabadon használható.

---

**Készítette:** GitHub Copilot
**Dátum:** 2026. április
**Verzió:** 1.0
