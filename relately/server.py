import os

from flask import Flask, request, jsonify

from . import engine

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

app = Flask('relately')
eng = engine.Engine()

@app.route("/select", methods=["POST"])
def select():
    return jsonify({"results":eng.select(request.get_json(force=True))})

@app.route("/select", methods=["GET"])
def selectget():
    return "GETME"
