from flask import jsonify
from app import app
from app.TFT_Api import TFT_Api

tft_api = TFT_Api()

@app.route('/')
@app.route('/index')
def index():
    return jsonify({"hello": "Hello, World!"})

@app.route('/top')
def top():
    return jsonify(tft_api.get_top_streams())