# app.py
from flask import Flask, render_template, request, jsonify
import time
import string
import itertools

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack_password():
    password = request.form['password']
    chars = string.ascii_lowercase
    attempts = 0

    start_time = time.time()
    for length in range(1, 5):  # Limit for demo
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            if ''.join(guess) == password:
                elapsed = time.time() - start_time
                return jsonify({
                    'password': password,
                    'attempts': attempts,
                    'time': round(elapsed, 2)
                })
    return jsonify({'error': 'Password not cracked'})

if __name__ == "__main__":
    app.run(debug=True)
