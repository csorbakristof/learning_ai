# A feladat

Díjbeszedős számla PDF-ekből adatkinyerés Python alatt. (Bár le lehet tölteni XML-ben is, így ez inkább csak tanulási kísérlet.)

Végül nagyjából elkészült, de nagyon nem teszteltem.

# Tanulságok

A PDF-ből adatkinyerés alapos tesztelést igényel. Pénzösszegben tizedesvessző, pont, szóköz bekavarnak. Elég sokat iterált az AI, de viszonylag magától.

Most kipróbáltam, hogy nem a spec.md-vel kezdtem, hanem csak egy rövid leírással és kérdezzen és utána azokat megválaszolva kezdődött a munka.

# Konkrét promptok

## Initial prompt without specs

I have several PDF files containing bills. I need to extract the following information:

- Amount of money to pay (price)
- Address of the consumer
- Provider company (like electricity, water etc.)
- Issue date of the bill

The file examples/Fotav_szamla_pelda.pdf and examples/MVM_gaz_szamla_pelda.pdf contain two samples.

examples/Fotav_szamla_pelda.pdf has a price 6267 Ft, issue date ("számla kelte" in hungarian) 2025.08.14., the provider ("Szolgáltató neve" in hungarian) is BKM Nonprofit Zrt., and the address of the consumer ("Felhasználási hely címe" in hungarian) is "1115 Budapest,Bartók Béla út 129/B.
3. em. 8".

What further information do you need to go along all PDF files in a directory and collect the information above from all of them, and export them into a CSV file? You should use python environment to do so.

## Additional information the AI asked for

The information you asked for:

1. PDF Processing Approach: I prefer text extraction
2. Language & Format Handling: all PDFs are in Hungarian. Date format is always YYYY.MM.DD, currency is always Ft.
3. Field Extraction Strategy: for provider detection, address and amount detection, look for the specific keywords but validate the detected strings and fallback to pattern matching if it failed.
4. Error Handling Preferences: log errors and mark as NOT_FOUND. If you can, mark uncertain extractions for human review.
5. Output Format:
CSV column names: Hungarian
Date output format in CSV is YYYY.MM.DD
Separator in CSV is semicolon ";".

## Create script (agent mode)

Now create the python script for me please.
