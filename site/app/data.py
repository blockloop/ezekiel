#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import sqlite3
from flask import g

_dbpath = '../../temperatures.db'


def query(queryStr, args=(), one=False):
    cur = _db().execute(queryStr, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def _db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(_dbpath, detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = _dict_factory
    return db


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
