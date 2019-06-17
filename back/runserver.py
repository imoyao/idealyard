#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from . import create_app, init_db

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
init_db(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
