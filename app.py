from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        return jsonify({"status": "success", "response": "test recommend"}), 200
    except:
        return jsonify({"status": "error", "response": "test recommend"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
