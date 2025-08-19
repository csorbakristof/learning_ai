# A feladat

Outlook makró készítése, mely az aktuális levél tartalmát két fájllal kiegészítve (egy saját kis backenden keresztül) megválaszoltatja a ChatGPT API-val (piszkozat feldobásával).

# Tanulságok

# Konkrét promptok

Have a look at the @workspace and summarize the outlook plugin and backend service it contains.

---

Now I want to deploy this application to my local machine. What steps do I need to take for that?

(Nagyon sok mindent elkészít hozzá... Próbál pl. SSL certet is létrehozni, bár nehezen sikerül...)
---
You mentioned "Update the path in sideload.ps1 to point to your manifest file". Please do that.
---

We are in a git repository. Please create a suitable .gitignore file.

# Start a dummy plugin

Hava a look at @overview.md. We are working on a desktop outlook plugin. As a separate plugin, create a new folder named "dummyplugin" and create a minimal functionality dummy plugin there. I want to test how a plugin is added to Outlook desktop. This dummy plugin should only add a button to outlook and if I press it, it should draft an email for me without sending it. The content of the drafted email should only contain "Hello world!".

