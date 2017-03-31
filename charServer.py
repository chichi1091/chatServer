# -*- coding: utf-8 -*-

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

run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), server=GeventWebSocketServer)
