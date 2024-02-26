from flask import Flask, jsonify, request
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/')
def home():
    return "Welcome to the Flask Web Application!"


@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        return jsonify({"message": "Send a POST request with data"})
    elif request.method == 'POST':
        data = request.json
        return jsonify({"received_data": data}), 201


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)