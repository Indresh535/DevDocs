from flask import Flask, render_template_string, request, redirect, session
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for session handling

# In-memory user example
users = {
    'admin': {
        'password': 'password123',
        'otp_secret': pyotp.random_base32()  # Store this in DB in real usage
    }
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect('/2fa')
        return 'Invalid credentials', 401

    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if 'username' not in session:
        return redirect('/')

    username = session['username']
    user = users[username]

    if request.method == 'POST':
        token = request.form['token']
        totp = pyotp.TOTP(user['otp_secret'])
        if totp.verify(token):
            return f"Logged in successfully as {username}"
        return "Invalid 2FA token", 403

    # Generate QR code for Google Authenticator setup
    totp = pyotp.TOTP(user['otp_secret'])
    otp_uri = totp.provisioning_uri(name=username, issuer_name="MyApp")
    qr = qrcode.make(otp_uri)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.getvalue()).decode()

    return render_template_string(f'''
        <p>Scan QR with Google Authenticator:</p>
        <img src="data:image/png;base64,{base64_img}"><br><br>
        <form method="post">
            Enter 2FA Code: <input name="token"><br>
            <input type="submit" value="Verify">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
