document.getElementById('crack-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    document.getElementById('result').innerHTML = `<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>`;
    document.getElementById('progress-container').style.display = 'block';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('progress-bar').innerText = '0%';

    const response = await fetch('/crack', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
        simulateCracking(result.attempts, result.password, result.time, result.hash);
    } else {
        document.getElementById('result').innerHTML = `❌ ${result.error}`;
        document.getElementById('progress-container').style.display = 'none';
    }
});

// Animate simulation
async function simulateCracking(attempts, crackedPassword, totalTime, hash) {
    document.getElementById('result').innerHTML = "";

    let attemptsMade = 0;
    const duration = totalTime * 1000;
    const delay = Math.max(duration / attempts, 10); // minimal delay

    while (attemptsMade < attempts) {
        attemptsMade++;
        let percent = Math.floor((attemptsMade / attempts) * 100);
        document.getElementById('progress-bar').style.width = `${percent}%`;
        document.getElementById('progress-bar').innerText = `${percent}%`;

        if (attemptsMade % Math.floor(attempts / 10) === 0) {
            document.getElementById('result').innerHTML = `🧪 Attempting password #${attemptsMade}...`;
        }

        await new Promise(resolve => setTimeout(resolve, delay));
    }

    document.getElementById('result').innerHTML = `
    ✅ Password Cracked: <strong>${crackedPassword}</strong><br>
    🧠 Hash: <small>${hash}</small><br>
    📈 Attempts: <strong>${attempts}</strong><br>
    ⏰ Time Taken: <strong>${totalTime} seconds</strong>`;

    document.getElementById('progress-bar').classList.remove('progress-bar-animated');
    document.getElementById('progress-bar').style.width = `100%`;
    document.getElementById('progress-bar').innerText = `Done`;
}

// Password Strength Meter
const passwordInput = document.getElementById('password');
const strengthBar = document.getElementById('strength-bar');

passwordInput.addEventListener('input', () => {
    const value = passwordInput.value;
    let strength = 0;

    if (value.length > 5) strength++;
    if (value.length > 8) strength++;
    if (/[A-Z]/.test(value)) strength++;
    if (/[0-9]/.test(value)) strength++;
    if (/[^A-Za-z0-9]/.test(value)) strength++;

    let width = (strength / 5) * 100;
    strengthBar.style.width = width + '%';

    if (strength <= 2) {
        strengthBar.className = 'progress-bar bg-danger';
    } else if (strength <= 4) {
        strengthBar.className = 'progress-bar bg-warning';
    } else {
        strengthBar.className = 'progress-bar bg-success';
    }
});
