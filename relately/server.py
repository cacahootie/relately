import os

from flask import Flask, request, jsonify

import engine

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

def get_instance(dbname=None, username=None, password=None, static_folder=None):
    app = Flask('relately', static_folder=os.path.join(basedir,'static'))
    eng = engine.Engine(dbname, username, password)

    @app.route("/select", methods=["POST"])
    def select():
        if request.args.get('mogrify'):
            return eng.select(request.get_json(force=True), mogrify=True)
        return jsonify({"results":eng.select(request.get_json(force=True))})

    @app.route("/select/<schema>/<view>", methods=["GET"])
    def select_get(schema, view):
        return jsonify({"results":eng.select({
            "columns":"*",
            "target":"{}.{}".format(schema,view)
        })})

    return app
