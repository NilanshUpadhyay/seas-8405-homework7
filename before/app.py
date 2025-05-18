from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Hard-coded password
PASSWORD = "supersecretpassword"

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Command injection vulnerability
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"error": "Missing IP address"}), 400
    try:
        # Direct shell execution for command injection
        result = subprocess.check_output(f"ping -c 1 {ip}", shell=True, text=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Ping failed: {e.output}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# Insecure use of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    if not expression:
        return jsonify({"error": "Missing expression"}), 400
    try:
        # Dangerous use of eval, no built-in restrictions
        result = eval(expression)
        return str(result)
    except Exception as e:
        return jsonify({"error": f"Calculation failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)