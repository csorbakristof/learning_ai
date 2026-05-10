# Feladat ötletek

## Python/C# feladatok:

1. **Pi közelítése Monte Carlo módszerrel** - Készíts LLM támogatással egy Python programot, amely véletlenszerű pontokat generál egy 1x1-es négyzetbe, és a pontoknak az egységnegyed körön belül/kívül esése alapján közelíti pi értékét.

2. **Szókitaláló játék (Wordle-szerű)** - Írasd meg LLM-mel Pythonban egy 5 betűs szó kitalálós játékot, ahol zöld/sárga/szürke visszajelzést ad a program a tippekhez.

3. **Számológép postfix notációval (RPN)** - Írasd meg LLM-mel C# nyelven egy Reverse Polish Notation számológépet (pl. "3 4 + 2 *" = 14).

4. **Tic-Tac-Toe konzolos játék** - Generáltass LLM segítségével Pythonban egy két játékos Tic-Tac-Toe játékot ASCII grafikával és győzelem detektálással.

## Vegyes feladatok:

5. **Scatter plot egységkörrel** - Készíts LLM támogatással Excel VBA makrót, amely az A és B oszlopokban lévő koordináta párokhoz scatter plotot készít, és a pontok színe piros vagy kék attól függően, hogy az egységkörön belül van-e.

6. **Szövegfájl tartalom statisztika** - Írasd meg LLM-mel Python programot, amely szövegfájlból számolja a sorok, szavak, karakterek számát, és listázza a 10 leggyakoribb szót.

## HTML+JavaScript single page alkalmazások:

7. **Színkeverő játék** - Készíttess LLM-mel egy HTML+JS appot, ahol RGB sliderekkelbeállítasz egy célszínt, és pontot kapsz aszerint, mennyire közel jársz egy véletlenszerűen generált színhez.

8. **BMI kalkulátor grafikonnal** - Írasd meg LLM-mel egy egyoldalas appot, amely kiszámolja a testtömegindexet, és színes skálán mutatja az eredményt (alulsúly/normál/túlsúly).

9. **Kő-papír-olló játék statisztikával** - Készíts LLM támogatással HTML+JS játékot a számítógép ellen, amely nyomon követi a győzelmeket/vereségeket és mutatja a stratégiádat.

10. **Jegyzettömb localStorage-dzsal** - Generáltass LLM-mel egy böngészős jegyzettömbappot, amely automatikusan menti a szöveget a localStorage-ba, így frissítés után is megmarad.

11. **Hex/RGB/HSL szín konverter** - Készíts LLM segítségével single page alkalmazást, amely valós időben konvertál a három színreprezentáció között, és megjeleníti a színt.

# Példa promptok a kiválasztott feladatokhoz

Kiválasztott feladatok: 3, 7, 10

## Feladat 3: Számológép postfix notációval (RPN) - C#

### Példa prompt:

```
Készíts egy C# konzol alkalmazást, amely Reverse Polish Notation (RPN) számológépként működik.

Követelmények:
1. A program kérjen be egy RPN kifejezést a felhasználótól (pl. "3 4 + 2 *")
2. A bevitelt szóközök mentén darabolja fel (split)
3. Egy stack (verem) segítségével értékelje ki a kifejezést:
   - Ha szám, tedd a verembe
   - Ha operátor (+, -, *, /), vegyél ki két számot a veremből, végezd el a műveletet, 
     és az eredményt tedd vissza a verembe
4. Az értékelés végén a veremben egyetlen szám marad - ez az eredmény
5. Kezelje a hibákat:
   - Érvénytelen input (nem szám és nem operátor)
   - Nincs elég operandus az operátorhoz
   - Nullával való osztás
6. A program fusson folyamatosan, amíg a felhasználó "exit"-et nem ír

Példa működés:
Input: 3 4 +
Output: 7

Input: 3 4 + 2 *
Output: 14

Input: 15 7 1 1 + - / 3 * 2 1 1 + + -
Output: 5

A kódot kommentekkel lásd el, hogy érthető legyen a működés.
Használj Stack<double> típust a számok tárolásához.
```

## Feladat 7: Színkeverő játék - HTML+JS

### Példa prompt:

```
Készíts egy single page HTML+JavaScript alkalmazást, amely egy színkeverő játék.

Játékmenet:
1. A program véletlenszerűen generál egy célszínt (RGB értékekkel)
2. A célszínt egy nagy színes négyzet formájában jelenítsd meg a képernyő tetején
3. Alatta 3 slider (csúszka) van: piros, zöld, kék (0-255 értéktartomány)
4. Egy második négyzet mutatja a sliderekkel beállított aktuális színt
5. Minden slider mozgatásakor frissül az aktuális szín
6. "Ellenőrzés" gomb megnyomásakor:
   - Számold ki a színek közötti távolságot az RGB térben: 
     Math.sqrt((r1-r2)² + (g1-g2)² + (b1-b2)²)
   - Maximális távolság: Math.sqrt(255² + 255² + 255²) ≈ 441
   - Pontszám: 100 * (1 - távolság/441) kerekítve
   - Jelenítsd meg a pontszámot és mennyire volt pontos (pl. "95 pont - Kiváló!")
7. "Új játék" gomb generál új célszínt
8. Számolja és jelenítse meg az átlagpontszámot az eddigi játékok alapján

Megjelenés:
- Modern, középre igazított design
- A célszín négyzet: 200x200 pixel
- Az aktuális szín négyzet: 200x200 pixel
- Sliderek szépen formázva, minden slider mellett az aktuális érték kijelzése
- Színes gombok
- Responsive, mobilon is jól nézzen ki

Technikai követelmények:
- Minden egy .html fájlban legyen (inline CSS és JavaScript)
- Ne használj külső library-kat, csak pure JavaScript
- A sliderek input type="range" legyenek
- Használj CSS flexbox-ot a layout-hoz
```

## Feladat 10: Jegyzettömb localStorage-dzsal - HTML+JS

### Példa prompt:

```
Készíts egy böngészőben futó jegyzettömb alkalmazást HTML+JavaScript segítségével, amely automatikusan menti és visszatölti a szöveget.

Funkciók:
1. Nagy textarea a szöveg szerkesztésére (teljes képernyő magasság nagy része)
2. Automatikus mentés localStorage-ba:
   - Minden gépelés után 1 másodperc késleltetéssel mentse el a tartalmat
   - Használj setTimeout/clearTimeout kombinációt a debounce-hoz
3. Oldal betöltésekor automatikusan töltse vissza a mentett szöveget
4. Jelenítsen meg egy státusz sort, amely mutatja:
   - Mikor történt az utolsó mentés (pl. "Utoljára mentve: 14:35:22")
   - Karakterek száma
   - Szavak száma (space-szel elválasztva)
5. Gombok:
   - "Új jegyzet" - törli a tartalmat (megerősítés után)
   - "Letöltés .txt fájlként" - letölti a szöveget txt fájlként
   - "Másolás vágólapra" - kimásolja a teljes szöveget
6. Dark mode kapcsoló (toggle gomb), ami szintén localStorage-ban perzisztens

Technikai részletek:
- localStorage kulcs: "notepad_content"
- localStorage dark mode kulcs: "notepad_darkmode"
- textarea automatikus átméretezés a tartalom szerint (vagy fixed full height)
- A mentés során vizuálisan jelezd (pl. zöld villogás vagy "Mentve" felirat)
- Használj modern CSS-t (flexbox/grid)
- Minden egy .html fájlban legyen
- Smooth animációk a dark mode váltáshoz

Példa státusz sor megjelenés:
"✓ Utoljára mentve: 15:42:08 | 1.234 karakter | 187 szó"

A dizájn legyen tiszta, minimalista, írásra optimalizált.
```

