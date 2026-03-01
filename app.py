from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def hello():
    return jsonify(
        message="✨ Welcome to flask-api ✨",
        tip="Built with Flask, shipped by Jenkins, running in Docker.",
        ui="Added new ui which is much better choose by Prite Dey"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
