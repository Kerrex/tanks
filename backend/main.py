#!/usr/bin/env python2

import tornado.ioloop
import tornado.websocket
import json
import engine
import players
import ident

from const import *


def dispatch_messages():
    if len(players.players) == 0:
        ident.clean_ids()
    for elem in players.players:
        elem.step(MESSAGE_TIME)
        for tank in engine.tanks:
            resp = {"id": engine.MSGID_UPDATE, "data": tank.export_delta()}
            elem.handler.write_message(resp)
        for bullet in engine.bullets:
            resp = {"id": engine.MSGID_UPDATE, "data": bullet.export_delta()}
            elem.handler.write_message(resp)
        for obstacle in engine.obstacles:
            resp = {"id": engine.MSGID_UPDATE, "data": obstacle.export_delta()}
            elem.handler.write_message(resp)
        for sprite in engine.deleted:
            resp = {"id": engine.MSGID_UPDATE, "data": sprite.export_delta()}
            elem.handler.write_message(resp)
    engine.deleted = []


class ServerHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Socket open")

    def on_message(self, message):
        msg = json.loads(message)
        if msg["id"] == engine.MSGID_REGISTER:
            player = players.register(self)
            print "Player %s registered." % player.nick
        elif msg["id"] == engine.MSGID_ACTION:
            tank = players.get_player_from_handler(self).tank
            if tank is not None:
                tank.act(msg["data"]["action_id"])

    def on_close(self):
        print "Socket closed - player %s unregistered." % players.get_player_from_handler(self).nick
        players.unregister(self)

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r"/", ServerHandler),
])
callback = tornado.ioloop.PeriodicCallback(dispatch_messages, MESSAGE_TIME)
callback.start()

ob = engine.obstacles.add()
ob.pos.x = engine.WIDTH / 2
ob.pos.y = engine.HEIGHT / 2
ob.mass = 10000.
ob.radius = 24.
ob = engine.obstacles.add()
ob.pos.x = engine.WIDTH / 2 - engine.WIDTH / 4
ob.pos.y = engine.HEIGHT / 2 - engine.HEIGHT / 4
ob.mass = 1000.
ob.radius = 16.
ob = engine.obstacles.add()
ob.pos.x = engine.WIDTH / 2 + engine.WIDTH / 4
ob.pos.y = engine.HEIGHT / 2 + engine.HEIGHT / 4
ob.mass = 1000.
ob.radius = 16.
ob = engine.obstacles.add()
ob.pos.x = engine.WIDTH / 2 + engine.WIDTH / 4
ob.pos.y = engine.HEIGHT / 2 - engine.HEIGHT / 4
ob.mass = 1000.
ob.radius = 16.
ob = engine.obstacles.add()
ob.pos.x = engine.WIDTH / 2 - engine.WIDTH / 4
ob.pos.y = engine.HEIGHT / 2 + engine.HEIGHT / 4
ob.mass = 1000.
ob.radius = 16.

if __name__ == "__main__":
    application.listen(8080)
    # tornado.ioloop.IOLoop.current().start()
    while (True):
        tornado.ioloop.IOLoop.current().run_sync(engine.process_physics)
