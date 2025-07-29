/*
Project: Outlook AI Email Assistant

🔍 Description:
This project is an Outlook Add-in combined with a local backend server to provide AI-assisted email triage, reply generation, and task planning using OpenAI’s GPT model. It includes both **Read** and **Compose** modes, allowing:

- Email classification (No action / Easy reply / Task required)
- AI-generated reply drafts for incoming messages
- AI-assisted writing for new messages or replies
- Integration with external markdown files as system context (workflow & customer info)
- Optional Power Automate or Outlook Rules-based automation (e.g., moving emails to folders)

---





---

📦 MSI Installer Instructions:

1. Use [Office Add-in Projects for Visual Studio](https://learn.microsoft.com/en-us/office/dev/add-ins/overview/office-add-ins) or [Yo Office generator](https://learn.microsoft.com/en-us/office/dev/add-ins/quickstarts/outlook-quickstart) to structure the project.
2. Use `wix` or `Advanced Installer` to wrap the manifest and static files.
3. Create self-signed cert for localhost access or configure reverse proxy to local backend.
4. Package manifest + static files and expose via https://localhost:3000

🚀 Deployment to Outlook Desktop:

1. Open Outlook > File > Options > Trust Center > Trust Center Settings > Add-ins
2. Click **Manage Add-ins** (opens browser)
3. Click **Upload Custom Add-in > Add from file...**, choose `manifest.xml`
4. Restart Outlook. Add-in will appear in reading and composing windows.

Let me know if you’d like a `.wxs` example for building the MSI with WiX Toolkit.
