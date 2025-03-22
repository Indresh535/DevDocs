#pip install flask authlib requests



from flask import Flask, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.tokens import BearerToken
from werkzeug.security import gen_salt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from authlib.integrations.sqla_oauth2 import (
    OAuth2AuthorizationCodeMixin,
    OAuth2ClientMixin,
    OAuth2TokenMixin
)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oauth.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class OAuth2Client(db.Model, OAuth2ClientMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class OAuth2Token(db.Model, OAuth2TokenMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


require_oauth = ResourceProtector()

class BearerToken(BearerToken):
    def create_token(self, client, grant_type, user, scope):
        return super().create_token(client, grant_type, user, scope)
    
authorization = AuthorizationServer(app, query_client=OAuth2Client.query)
authorization.register_grant(AuthorizationCodeGrant)
authorization.init_app(app)

# Best Practices for Secure Decryption
# ✅ Never store the encryption key in the client’s code.
# ✅ Retrieve the key dynamically from a secure key store (e.g., AWS KMS, HashiCorp Vault, Azure Key Vault).
# ✅ Use HTTPS/TLS 1.2+ to encrypt all communications.
# ✅ Log access attempts but never log decrypted credit card data.

# 🚀 Secure Flow for Decryption
# 1️⃣ Client authenticates via OAuth 2.0 and gets an access token.
# 2️⃣ Client requests encrypted credit card data from the API.
# 3️⃣ Client requests a decryption key securely from the API.
# 4️⃣ Client decrypts the data in memory (never store it permanently).


#  Client authenticates via OAuth 2.0 and gets an access token.
# 2️⃣ Client requests encrypted credit card data from the API.
# 3️⃣ Client requests a decryption key securely from the API.
# 4️⃣ Client decrypts the data in memory (never store it permanently).


# 🔹 Best Practices for Secure Decryption
# ✔️ Never store the encryption key in your client-side code.
# ✔️ Always request the key securely from a Key Management System (KMS).
# ✔️ Use HTTPS/TLS 1.2+ to protect data in transit.
# ✔️ Restrict access to decryption keys using Role-Based Access Control (RBAC).
# ✔️ Use tokenization instead of storing raw credit card numbers.