import os

from flask import Flask, request, jsonify

from . import engine

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

app = Flask('relately')
eng = engine.Engine()

@app.route("/select", methods=["POST"])
def select():
    if request.args.get('mogrify'):
        return eng.select(request.get_json(force=True), mogrify=True)
    return jsonify({"results":eng.select(request.get_json(force=True))})

@app.route("/select/<schema>/<table>", methods=["GET"])
def select_get(schema, table):
    return jsonify({"results":eng.select({
        "columns":"*",
        "target":"{}.{}".format(schema,table)
    })})

