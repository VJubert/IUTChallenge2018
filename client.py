# !/usr/bin/env python3
import asyncio
import json
import random
import sys
import argparse

from Map import *
from joueur import Joueur
from PathFindinf import *


class ClientConcoursProg(asyncio.Protocol):

    def __init__(self, loop):
        self.loop = loop
        self.state = 0
        self.liste_actions = [("move", "shoot"), ("move",),
                              ("move",), ("move",), ("hrotate",)]
        self.monde = {}
        self.map = None
        self.joueurs = {}
        self.idJoueur = -1

    def connection_made(self, transport):
        self.transport = transport
        print("Connecté")
        self.send_message({"nickname": "Tester C'est Douter !"})

    def data_received(self, data):
        for d in data.decode().strip().split("\n"):
            self.traite_donnees(json.loads(d))

    def traite_donnees(self, donnees):
        if "idJoueur" in donnees:
            self.idJoueur = donnees["idJoueur"]
            self.joueurs[self.idJoueur] = Joueur(self.idJoueur, None, None)
        if "map" in donnees:
            self.monde = donnees
            self.map = Map(donnees)
            for j in donnees["joueurs"]:
                id = j["id"]
                position = j["position"]
                direction = j["direction"]
                if id in self.joueurs:
                    self.joueurs[id].update(position, direction)
                else:
                    self.joueurs[id] = Joueur(id, position, direction)

                # todo create joueur
                None
        aStar(self.joueur[self.idJoueur].position,(0,0))
        print(self.joueurs)
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
