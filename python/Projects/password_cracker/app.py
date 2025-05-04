from flask import Flask, render_template, request, jsonify
import time
import string
import itertools
import random
import hashlib
import json

app = Flask(__name__)

# Load a dictionary of common passwords
with open('dictionary.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

# Load a simulated rainbow table
try:
    with open('rainbow_table.json', 'r') as f:
        rainbow_table = json.load(f)
except FileNotFoundError:
    rainbow_table = {}

def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack_password():
    password = request.form['password']
    attack_type = request.form['attack_type']
    hashed = request.form.get('hashed', 'false') == 'true'

    attempts = 0
    found = False
    guess = ""
    start_time = time.time()

    target = password
    #if hashed:
    target_hash = generate_hash(password)

    if attack_type == "brute_force":
        chars = string.ascii_lowercase + string.digits
        for length in range(1, 5):  
            for attempt in itertools.product(chars, repeat=length):
                guess = ''.join(attempt)
                attempts += 1
                if (guess == password and not hashed) or (generate_hash(guess) == target_hash and hashed):
                    found = True
                    break
            if found:
                break

    elif attack_type == "dictionary":
        for word in common_passwords:
            attempts += 1
            if (word == password and not hashed) or (generate_hash(word) == target_hash and hashed):
                guess = word
                found = True
                break

    elif attack_type == "smart_dictionary":
        mutations = []
        for word in common_passwords:
            mutations.extend([
                word, word+"123", word.replace('o','0'), word.replace('a','@'), word.capitalize()
            ])
        for word in mutations:
            attempts += 1
            if (word == password and not hashed) or (generate_hash(word) == target_hash and hashed):
                guess = word
                found = True
                break

    elif attack_type == "masked":
        for letter in string.ascii_lowercase:
            for num in range(100):
                guess = f"{letter}{num:02d}"
                attempts += 1
                if (guess == password and not hashed) or (generate_hash(guess) == target_hash and hashed):
                    found = True
                    break
            if found:
                break

    elif attack_type == "rainbow":
        if hashed:
            guess = rainbow_table.get(target_hash)
            attempts = 1
            found = guess is not None
        else:
            return jsonify({
                'error': 'Rainbow table attack requires a hashed password!',
                'success': False
            })

    elapsed = time.time() - start_time

    if found:
        return jsonify({
            'password': guess,
            'attempts': attempts,
            'time': round(elapsed, 2),
            'success': True,
            'weak_password': True,
            'hash': generate_hash(guess),
            'message': 'Password successfully cracked! This is a weak password.'
        })
    else:
        return jsonify({
            'error': 'Password not cracked after many attempts',
            'success': False
        })

if __name__ == "__main__":
    app.run(debug=True)
