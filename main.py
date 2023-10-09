import secrets
from geopy.distance import great_circle
from Analisis import execute_analize
from prediction import prediction
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/get_past_peeks/',methods=['GET'])
def get_past_peeks():

    analize = execute_analize()
    result = analize
    return jsonify(result)

@app.route('/predictions/',methods=['GET'])
def predictions():

    analize = prediction()
    result = analize
    return jsonify(result)

if __name__ == "_main_":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
