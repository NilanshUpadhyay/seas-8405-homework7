from flask import Flask, request, jsonify
import os
import subprocess
import ast
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
PASSWORD = os.getenv("APP_PASSWORD")

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name: alphanumeric only"}), 400
    return f"Hello, {name}!"

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    # Input validation: ensure IP is in valid format
    if not ip or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip.split('.')) or len(ip.split('.')) != 4:
        return jsonify({"error": "Invalid IP address"}), 400
    try:
        # Use parameterized command, avoid shell=True
        result = subprocess.check_output(["ping", "-c", "1", ip], text=True)
        return result
    except subprocess.CalledProcessError:
        return jsonify({"error": "Ping failed"}), 500

@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    # Input validation: allow only basic math expressions
    if not expression or not all(c.isdigit() or c in "+-*/" for c in expression.replace(" ", "")):
        return jsonify({"error": "Invalid expression: only digits and +-*/ allowed"}), 400
    try:
        # Use ast.literal_eval for safe evaluation
        result = ast.literal_eval(expression)
        if not isinstance(result, (int, float)):
            return jsonify({"error": "Expression must evaluate to a number"}), 400
        return str(result)
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid expression"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
