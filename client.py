# !/usr/bin/env python3
import asyncio
import json
import random
import sys
import argparse

from game import Game


class ClientConcoursProg(asyncio.Protocol):

    def __init__(self, loop):
        self.game = Game()
        self.loop = loop
        # self.state = 0
        # self.liste_actions = [("move", "shoot"), ("move",),
        #                       ("move",), ("move",), ("hrotate",)]

    def connection_made(self, transport):
        self.transport = transport
        self.send_message({"nickname": "TestCDout!"})

    def data_received(self, data):
        for d in data.decode().strip().split("\n"):
            self.traite_donnees(json.loads(d))

    def traite_donnees(self, donnees):
        # action = self.liste_actions[self.state]
        # self.state = (self.state + 1) % len(self.liste_actions)
        # self.send_message(action)
        to_send = self.game.play(donnees)
        if to_send is not None:
            self.send_message(to_send)

    def connection_lost(self, exc):
        self.loop.stop()

    def send_message(self, message):
        self.transport.write(json.dumps(message).encode() + b'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="IA concours de programmation")
    parser.add_argument("hostname", help="Nom ou adresse IP du serveur de jeu")
    parser.add_argument("-p", dest="port", default=8889,
                        type=int, help="Port du serveur auquel se connecter")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()

    coro = loop.create_connection(
        lambda: ClientConcoursProg(loop), args.hostname, args.port
    )

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
