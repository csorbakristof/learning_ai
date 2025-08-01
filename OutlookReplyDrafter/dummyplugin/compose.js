Office.onReady(info => {
    if (info.host === Office.HostType.Outlook) {
        document.getElementById("draft-hello-world").onclick = draftHelloWorldEmail;
        updateStatus("Plugin ready! Click the button to draft a Hello World email.");
    } else {
        updateStatus("This plugin only works in Outlook.");
    }
});

function draftHelloWorldEmail() {
    const button = document.getElementById("draft-hello-world");
    button.disabled = true;
    updateStatus("Drafting Hello World email...");

    try {
        const item = Office.context.mailbox.item;

        // Set the subject
        item.subject.setAsync("Hello World from Dummy Plugin", (result) => {
            if (result.status === Office.AsyncResultStatus.Failed) {
                updateStatus("Error setting subject: " + result.error.message);
                button.disabled = false;
                return;
            }
            
            // Set the body content
            item.body.setAsync(
                "Hello world!",
                {
                    coercionType: Office.CoercionType.Text
                },
                (result) => {
                    if (result.status === Office.AsyncResultStatus.Failed) {
                        updateStatus("Error setting body: " + result.error.message);
                    } else {
                        updateStatus("Hello World email drafted successfully! ✓");
                    }
                    button.disabled = false;
                }
            );
        });
        
    } catch (error) {
        updateStatus("Error: " + error.message);
        button.disabled = false;
    }
}

function updateStatus(message) {
    const statusDiv = document.getElementById("status");
    statusDiv.textContent = message;
    statusDiv.style.color = message.includes("Error") ? "red" : "green";
}
