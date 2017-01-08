#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
