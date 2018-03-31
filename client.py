# !/usr/bin/env python3
import asyncio
import json
import random
import sys
import argparse

from joueur import Joueur
from PathFinding import *


class ClientConcoursProg(asyncio.Protocol):

    def __init__(self, loop):
        self.loop = loop
        self.state = 0
        self.liste_actions = [("move", "shoot"), ("move",),
                              ("move",), ("move",), ("hrotate",)]
        self.monde = {}
        self.map = None
        self.joueurs = {}
        self.projectiles = {}
        self.idJoueur = -1

    def connection_made(self, transport):
        self.transport = transport
        print("Connecte")
        self.send_message({"nickname": "Tester C'est Douter !"})

    def data_received(self, data):
        for d in data.decode().strip().split("\n"):
            self.traite_donnees(json.loads(d))

    def traite_donnees(self, donnees):
        print("         NEW TURN            ")
        print(self.joueurs)
        print(self.projectiles)
        print(donnees)
        if "idJoueur" in donnees:
            self.idJoueur = donnees["idJoueur"]
            self.joueurs[self.idJoueur] = Joueur(self.idJoueur, None, None)
            return
        if "map" in donnees:
            self.monde = donnees
            self.map = Map.Map(donnees)
            for j in donnees["joueurs"]:
                id = j["id"]
                position = j["position"]
                direction = j["direction"]
                if id in self.joueurs:
                    self.joueurs[id].update(position, direction)
                else:
                    self.joueurs[id] = Joueur(id, position, direction)
            return

        for msg in donnees:
            if "projectile" in msg:
                action = msg[1]
                id = msg[2]
                if "move" == action:
                    newPos = msg[3]
                    (pos, dir) = self.projectiles[id]
                    self.projectiles[id] = (newPos, dir)
                if "explode" == action:
                    pos = msg[3]
                    posList = msg[4]
                    tankDone = msg[5]
                    del (self.projectiles[id])
            if "shoot" in msg:
                idjoueur = msg[0]
                idproj = msg[2]
                pos = msg[3]
                dir = msg[4]
                self.projectiles[idproj] = (pos, dir)

        # aStar(self.map, self.joueurs[self.idJoueur].current_pos(), (0, 0))

        if self.map is not None:
            self.map.update(donnees)

        action = self.liste_actions[self.state]
        self.state = (self.state + 1) % len(self.liste_actions)
        self.send_message(action)

    def connection_lost(self, exc):
        self.loop.stop()

    def send_message(self, message):
        self.transport.write(json.dumps(message).encode() + b'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="IA concours de programmation")
    parser.add_argument("hostname", help="Nom ou adresse IP du serveur de jeu")
    parser.add_argument("-p", dest="port", default=8889,
                        type=int, help="Port du serveur auquel se connecter")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()

    coro = loop.create_connection(
        lambda: ClientConcoursProg(loop), args.hostname, args.port)

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
