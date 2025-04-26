from flask import Flask, render_template, request, jsonify
import time
import string
import itertools
import random

app = Flask(__name__)

# Load a dictionary of common passwords
with open('dictionary.txt', 'r') as f:
    common_passwords = [line.strip() for line in f.readlines()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack_password():
    password = request.form['password']
    attack_type = request.form['attack_type']
    attempts = 0
    found = False
    guess = ""
    start_time = time.time()

    if attack_type == "brute_force":
        chars = string.ascii_lowercase + string.digits
        for length in range(1, 5):  # Limit for demo
            for attempt in itertools.product(chars, repeat=length):
                guess = ''.join(attempt)
                attempts += 1
                if guess == password:
                    found = True
                    break
            if found:
                break

    elif attack_type == "dictionary":
        for word in common_passwords:
            attempts += 1
            if word == password:
                guess = word
                found = True
                break

    elif attack_type == "smart_dictionary":
        # Try simple mutations (like adding 123, replacing o with 0)
        mutations = []
        for word in common_passwords:
            mutations.append(word)
            mutations.append(word + "123")
            mutations.append(word.replace('o', '0'))
            mutations.append(word.replace('a', '@'))
            mutations.append(word.capitalize())

        for word in mutations:
            attempts += 1
            if word == password:
                guess = word
                found = True
                break

    elif attack_type == "masked":
        # Guess common patterns (e.g., letter + 2 numbers)
        for letter in string.ascii_lowercase:
            for num in range(100):
                guess = f"{letter}{num:02d}"
                attempts += 1
                if guess == password:
                    found = True
                    break
            if found:
                break

    elapsed = time.time() - start_time

    if found:
        return jsonify({
            'password': guess,
            'attempts': attempts,
            'time': round(elapsed, 2),
            'success': True
        })
    else:
        return jsonify({
            'error': 'Password not cracked after many attempts',
            'success': False
        })

if __name__ == "__main__":
    app.run(debug=True)
