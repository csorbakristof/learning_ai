// --- outlook-addin/compose.js ---
Office.onReady(() => {
  document.getElementById("improve").onclick = () => {
    const draft = document.getElementById("draft").value;
    fetch("http://localhost:5000/compose-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ draft })
    })
      .then(res => res.json())
      .then(data => {
        Office.context.mailbox.item.body.setAsync(data.response, { coercionType: "html" });
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error improving email: ' + error.message);
      });
  };
});
