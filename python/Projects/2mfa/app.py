from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp, qrcode, io, base64

app = Flask(__name__)
app.secret_key = 'supersecret'

# In-memory user store
# users = {}
users = {
    'admin': {
        'password_hash': generate_password_hash('pass123'),
        'otp_secret': pyotp.random_base32()  # Hardcoded secret (or generate a new one)
    }
}

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return 'User already exists', 409

        otp_secret = pyotp.random_base32()
        hashed_pw = generate_password_hash(password)

        users[username] = {
            'password_hash': hashed_pw,
            'otp_secret': otp_secret
        }
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            return redirect(url_for('verify'))
        return 'Invalid credentials', 401

    return render_template('login.html')

# TOTP Verification
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = users.get(username)
    totp = pyotp.TOTP(user['otp_secret'])

    if request.method == 'POST':
        code = request.form['code']
        if totp.verify(code):
            return f"🎉 Logged in as {username}"
        else:
            return "Invalid 2FA code", 403

    # QR Code for setup
    uri = totp.provisioning_uri(name=username, issuer_name="SecureApp")
    qr = qrcode.make(uri)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    qr_base64 = base64.b64encode(buf.getvalue()).decode()

    return render_template('verify.html', qr_image=qr_base64)

if __name__ == '__main__':
    app.run(debug=True)





# Simple TOTPO AUTH
# from flask import Flask, render_template_string, request, redirect, session
# import pyotp
# import qrcode
# import io
# import base64

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'  # for session handling

# # In-memory user example
# users = {
#     'admin': {
#         'password': 'password123',
#         'otp_secret': pyotp.random_base32()  # Store this in DB in real usage
#     }
# }

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = users.get(username)
#         if user and user['password'] == password:
#             session['username'] = username
#             return redirect('/2fa')
#         return 'Invalid credentials', 401

#     return render_template_string('''
#         <form method="post">
#             Username: <input name="username"><br>
#             Password: <input type="password" name="password"><br>
#             <input type="submit" value="Login">
#         </form>
#     ''')

# @app.route('/2fa', methods=['GET', 'POST'])
# def two_factor():
#     if 'username' not in session:
#         return redirect('/')

#     username = session['username']
#     user = users[username]

#     if request.method == 'POST':
#         token = request.form['token']
#         totp = pyotp.TOTP(user['otp_secret'])
#         if totp.verify(token):
#             return f"Logged in successfully as {username}"
#         return "Invalid 2FA token", 403

#     # Generate QR code for Google Authenticator setup
#     totp = pyotp.TOTP(user['otp_secret'])
#     otp_uri = totp.provisioning_uri(name=username, issuer_name="MyApp")
#     qr = qrcode.make(otp_uri)
#     img_io = io.BytesIO()
#     qr.save(img_io, 'PNG')
#     img_io.seek(0)
#     base64_img = base64.b64encode(img_io.getvalue()).decode()

#     return render_template_string(f'''
#         <p>Scan QR with Google Authenticator:</p>
#         <img src="data:image/png;base64,{base64_img}"><br><br>
#         <form method="post">
#             Enter 2FA Code: <input name="token"><br>
#             <input type="submit" value="Verify">
#         </form>
#     ''')

# if __name__ == '__main__':
#     app.run(debug=True)
