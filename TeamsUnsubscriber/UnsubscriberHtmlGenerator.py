"""
Generate an interactive HTML page listing your joined Microsoft Teams.
All teams are preselected with checkboxes.
You can uncheck the ones you want to keep and copy the leave links.

Requirements:
    pip install msal requests
Usage:
    python list_teams_interactive.py
"""

import msal
import requests
import html
import json

# === CONFIGURATION ===
CLIENT_ID = "YOUR_CLIENT_ID_HERE"  # replace with your app id
TENANT = "organizations"
SCOPES = ["User.Read", "Team.ReadBasic.All"]

AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# === AUTHENTICATION ===
app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    raise Exception("Device code flow initiation failed")

print(flow["message"])
result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    raise SystemExit("Authentication failed: " + str(result.get("error_description")))

headers = {"Authorization": f"Bearer {result['access_token']}"}

# === FETCH TEAMS ===
print("Retrieving your joined Teams...")
resp = requests.get(f"{GRAPH_BASE}/me/joinedTeams", headers=headers)
resp.raise_for_status()
teams = resp.json().get("value", [])
print(f"Found {len(teams)} teams.")

# === BUILD HTML ===
team_data = []
for t in teams:
    name = html.escape(t.get("displayName", "<no name>"))
    tid = t["id"]
    link = f"https://teams.microsoft.com/l/team/{tid}/conversations?groupId={tid}"
    team_data.append({"name": name, "link": link})

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>My Microsoft Teams</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 2em; }}
h1 {{ color: #333; }}
button {{ margin: 1em 0; padding: 0.5em 1em; font-size: 1em; }}
ul {{ list-style-type: none; padding: 0; }}
li {{ margin-bottom: 0.5em; }}
label {{ cursor: pointer; }}
a {{ color: #0078d7; text-decoration: none; margin-left: 0.5em; }}
a:hover {{ text-decoration: underline; }}
pre {{
  background: #f5f5f5; padding: 1em; white-space: pre-wrap;
  border: 1px solid #ccc; display: none;
}}
</style>
</head>
<body>
<h1>Your Microsoft Teams</h1>
<p>Uncheck any teams you want to keep. Then click "Copy leave links" to copy
the Teams URLs for manual leaving.</p>

<button id="copyBtn">Copy leave links</button>
<pre id="output"></pre>

<ul>
"""

for i, t in enumerate(team_data):
    html_content += (
        f"<li><label><input type='checkbox' class='teambox' checked "
        f"data-link='{t['link']}'/> {t['name']}</label>"
        f"<a href='{t['link']}' target='_blank'>[Open]</a></li>\n"
    )

html_content += """</ul>

<script>
document.getElementById('copyBtn').addEventListener('click', async () => {
  const boxes = document.querySelectorAll('.teambox');
  const selected = [];
  boxes.forEach(b => { if (b.checked) selected.push(b.dataset.link); });
  const text = selected.join('\\n');
  try {
    await navigator.clipboard.writeText(text);
    alert(selected.length + " link(s) copied to clipboard!");
  } catch(e) {
    const out = document.getElementById('output');
    out.textContent = text;
    out.style.display = 'block';
    alert("Clipboard copy not supported — links shown below.");
  }
});
</script>
</body>
</html>"""

# === WRITE OUTPUT ===
with open("teams_to_leave.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Generated: teams_to_leave.html")
print("Open it in your browser to select which teams to leave.")
