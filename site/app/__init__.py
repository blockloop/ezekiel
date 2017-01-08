#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from flask import g, Flask, render_template, jsonify, request
from data import query
app = Flask(__name__, static_url_path='/assets', static_folder='./assets')


@app.route('/')
def root():
    return render_template('index.html', title="Temps")


@app.route('/api/current_temp', methods=['GET', 'POST'])
def current_temp():
    item = query("SELECT * FROM temperatures ORDER BY modified DESC LIMIT 1", one=True)
    if request.method == 'GET':
        return jsonify(item)
    elif request.method == 'POST':
        return jsonify({
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "%d degrees" % item['probe_f']
                },
                "shouldEndSession": True
            },
            "sessionAttributes": {}
        })


@app.route('/api/temps')
def temps():
    items = query("SELECT * FROM temperatures ORDER BY modified ASC")
    return jsonify({"temperatures": items})


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


