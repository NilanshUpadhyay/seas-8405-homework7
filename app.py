from flask import Flask, request, jsonify
import ast
import re
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get secret from environment variable
PASSWORD = os.getenv("PASSWORD")

def is_valid_ip(ip):
    """Validate IP address format."""
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(pattern, ip))

def is_valid_expr(expr):
    """Validate mathematical expression."""
    pattern = r'^[0-9+\-*/(). ]+$'
    return bool(re.match(pattern, expr))

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    # Require password for authentication
    if not PASSWORD or request.args.get('password') != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip or not is_valid_ip(ip):
        return jsonify({"error": "Invalid or missing IP address"}), 400
    # Require password for authentication
    if not PASSWORD or request.args.get('password') != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Safe subprocess without shell=True
        result = subprocess.run(
            ['ping', '-c', '1', ip],  # Use '-c' for Linux
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({"output": result.stdout})
    except subprocess.SubprocessError:
        return jsonify({"error": "Ping failed"}), 500

@app.route('/calculate')
def calculate():
    expr = request.args.get('expr')
    if not expr or not is_valid_expr(expr):
        return jsonify({"error": "Invalid or missing expression"}), 400
    # Require password for authentication
    if not PASSWORD or request.args.get('password') != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Use ast.literal_eval instead of eval
        result = ast.literal_eval(expr)
        return jsonify({"result": result})
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid expression"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)