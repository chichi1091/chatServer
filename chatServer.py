# -*- coding: utf-8 -*-

import os
from bottle import get, template, run
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

users = set()

@get('/')
def index():
    return template('views/index')

@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else:
            break
    users.remove(ws)

if os.getenv("HEROKU")==None:
    run(host="localhost", port=(os.environ.get("PORT", 5200)), server=GeventWebSocketServer, debug=True, reloader=True)
else:
    run(host="0.0.0.0", port=(os.environ.get("PORT", 5200)), server=GeventWebSocketServer)
