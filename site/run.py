import sqlite3
from datetime import datetime
from flask import g, Flask, render_template, jsonify, request

app = Flask(__name__, static_url_path='/assets', static_folder='./assets')

DATABASE = '../temperatures.db'


@app.route('/')
def root():
    return render_template('index.html', title="Temps")


@app.route('/api/current_temp', methods=['GET', 'POST'])
def current_temp():
    item = query_db("SELECT * FROM temperatures ORDER BY modified ASC LIMIT 1", one=True)
    if request.method == 'POST':
        return jsonify({
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "%6.2f degrees" % item.probe_f
                },
                "shouldEndSession": True
            },
            "sessionAttributes": {}
        })
    elif request.method == 'GET':
        return jsonify(item)


@app.route('/api/temps')
def temps():
    items = query_db("SELECT * FROM temperatures ORDER BY modified ASC")
    return jsonify({"temperatures": items})


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
    
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
