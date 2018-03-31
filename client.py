#!/usr/bin/env python3
import asyncio
import json
import random
import sys
import argparse²

class Joueur :
    #pile des positions
    positions=[]
    #0 nord / 1 est / 2 sud / 3 ouest
    direction=0
    id=0
    score=0

    def __init__(self, id, pos, rot):
        self.id=id;
        self.positions.insert(0,pos)-
        if rot == [0,1]:
            self.direction=3
        else if rot == [0,-1]:
            self.direction=1
        else if rot == [1,0]:
            self.direction=2
        else if rot == [-1,0]:
            self.direction=0

    def __init__(self, id):
        self.id=id;

    def update(self, position):
        self.score=score;
        self.positions.insert(0,position):

    def is_safe(self):
        False


class ClientConcoursProg(asyncio.Protocol):

    def __init__(self, loop):
        self.loop = loop
        self.state = 0
        self.liste_actions = [("move", "shoot"), ("move",),
                              ("move",), ("move",), ("hrotate",)]
        self.monde = {}
        self.joueurs={}
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
            self.joueurs[id]=Joueur(self.idJoueur)
        if "map" in donnees:
            self.monde = donnees
            print("Nombre d'objets dans la carte :" + str(len(donnees["map"])))
            print("Joueurs :" + str(donnees["joueurs"]))
            for j in donnees["joueurs"]:
                if(j["id"] == self.idJoueur):
                    print("Position :" + str(j["position"]))
        action = self.liste_actions[self.state]
        self.state = (self.state + 1) % len(self.liste_actions)
        self.send_message(action)

    def connection_lost(self, exc):
        self.loop.stop()

    def send_message(self, message):
        self.transport.write(json.dumps(message).encode() + b'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="IA concours de programmation")
    parser.add_argument("hostname", help="Nom ou adresse IP du serveur de jeu")
    parser.add_argument("-p", dest="port", default=8889,type=int, help="Port du serveur auquel se connecter")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()

    coro = loop.create_connection(lambda: ClientConcoursProg(loop), args.hostname, args.port)

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
