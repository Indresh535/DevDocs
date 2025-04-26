document.getElementById('crack-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    document.getElementById('result').innerHTML = "🧠 Cracking... Please wait...";

    const response = await fetch('/crack', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
        document.getElementById('result').innerHTML = `
        ✅ Password Cracked: <strong>${result.password}</strong><br>
        📈 Attempts: <strong>${result.attempts}</strong><br>
        ⏰ Time Taken: <strong>${result.time} seconds</strong>`;
    } else {
        document.getElementById('result').innerHTML = `❌ ${result.error}`;
    }
});
