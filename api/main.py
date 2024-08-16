# Flask API
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/search", methods=["POST"])

def search():
    results = []
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)