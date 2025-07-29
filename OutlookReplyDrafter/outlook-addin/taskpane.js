// --- outlook-addin/taskpane.js ---
Office.onReady(info => {
  if (info.host === Office.HostType.Outlook) {
    document.getElementById("process-email").onclick = () => {
      const item = Office.context.mailbox.item;
      item.body.getAsync("text", result => {
        const emailContent = result.value;

        fetch("http://localhost:5000/analyze-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subject: item.subject,
            sender: item.from.emailAddress,
            body: emailContent
          })
        })
          .then(response => response.json())
          .then(data => {
            const output = document.getElementById("output");
            output.innerHTML = `<h3>AI Analysis:</h3><p>${data.response}</p>`;
            
            // Create reply with AI suggestion
            item.displayReplyFormAsync(`AI-suggested reply:\n${data.response}`);
            
            // Optional: Flag and categorize the email
            item.flag.setAsync({ flagStatus: "flagged" });
            item.categories.addAsync(["AI-Processed"]);
          })
          .catch(error => {
            document.getElementById("output").innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
          });
      });
    };
  }
});
