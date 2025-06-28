from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask app!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 