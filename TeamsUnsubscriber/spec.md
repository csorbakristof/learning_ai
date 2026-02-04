# Használati útmutató

App-regisztráció az Azure Entra admin centerben:
- „New registration” → nevet adsz (pl. TeamsListScript).
- Supported account types: Accounts in this organizational directory only.
- Nincs szükség redirect URI-ra.
- Jegyezd meg a Client ID-t, és írd be a script elejére.
- API permissions:
  - User.Read
  - Team.ReadBasic.All (mind delegált, nincs admin consent szükség).

Futtatás

```
pip install msal requests
python list_teams_interactive.py
```

Jelentkezz be
- A script kiír egy üzenetet pl.:

```
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code XXXXXXXX
```

- Menj a linkre, írd be a kódot, jelentkezz be a saját fiókoddal.

Eredmény

- Megjelenik a teams_to_leave.html fájl.
- Nyisd meg böngészőben → minden csapat mellett látszik: ✅ checkbox + 🔗 [Open] link.
- Pipáld ki, amiből ki akarsz lépni, majd nyomd meg a Copy leave links gombot.
- A linkek bekerülnek a vágólapra (vagy megjelennek a lapon), és onnan Teamsben megnyitva kézzel kiléphetsz.
