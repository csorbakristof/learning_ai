# Tanulságok

- Nagyon lassú és el is száll az első implementáció. Minden karakterre egyesével vizsgál háttérszínt és töröl, ha kell.
- A spec.md Details részében az AI kérdéseire adtam választ.
- Meg kellett volna kérni, hogy hagyja ki a hibakezelést.

# Konkrét promptok

### This macro seems to be very slow. Can you use a solution which runs faster? For example by searching for yellow highlights in advance?

Wow, a válaszában aszimptotikus futásidő van!!!

"Performance Optimization:

- Uses Find.Execute to locate only yellow highlighted/shaded text instead of checking every character
- Changes algorithm from O(n) where n=total characters to O(m) where m=yellow ranges (typically much smaller)
- Only processes matches found by Find, dramatically reducing iterations"

### I get the error message that an object does not exist because the object references to the end of a table row.

Javította egyből.
