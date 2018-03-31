# !/usr/bin/env python3
import asyncio
import json
import random
import sys
import argparse

import Map
from joueur import Joueur, cast_rot_inverse
from PathFinding import *
from moves import *


class ClientConcoursProg(asyncio.Protocol):

    def __init__(self, loop):
        self.accu = b""
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
        self.send_message({"nickname": "TestCDout!"})

    def data_received(self, data):
        self.accu += data
        try:
            for d in self.accu.decode().strip().split("\n"):
                self.traite_donnees(json.loads(d))
            self.accu = b""
        except Exception as e:
            print(e)
            pass

    def traite_donnees(self, donnees):

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
                    cell = self.map.get_at(*pos)
                    if tankDone:
                        j = cell.joueur
                        j.positions = []
                        cell.joueur = None

                    for pos_mur in posList:
                        mur = self.map.get_at(*pos_mur)
                        mur.cassable = None

                    del (self.projectiles[id])
            if "shoot" in msg:
                idjoueur = msg[2]
                idproj = msg[3]
                pos = msg[4]
                dir = msg[5]
                self.projectiles[idproj] = (pos, dir)

        if self.map is not None:
            self.map.update(donnees)
            joueur = self.map.get_joueur(self.idJoueur)

            for id, (pos, dir) in self.projectiles.items():
                coming = self.proj_coming((pos, dir), joueur, self.map)
                if coming > -1:
                    cost = cost_orientation(
                        joueur.direction, self.calc_retourne(joueur, pos))
                    if cost < coming:
                        # retourne et tire
                        self.send_message(
                            [rotate_to(cast_rot_inverse(joueur.direction), rotation_requise(joueur.current_pos(), pos)),
                             "shoot"])
                        return
                        

            moi = self.map.get_joueur(self.idJoueur)
            ma_pos = moi.current_pos()

            dest = self.map.position_bonus()
            if dest is None:
                dest_joueurs = [pos for pos in self.map.position_joueurs(
                ) if pos is not None and pos != ma_pos]

                if len(dest_joueurs) == 0:
                    dest = (self.map.bornes[0] // 2, self.map.bornes[1] // 2)
                else:
                    dest = dest_joueurs[0]

            path = aStar(self.map, ma_pos, dest)

            if len(path) > 0:
                # shoot = self.map.get_at(*path[0]).est_mur_traversabel()

                rot_req = rotation_requise(ma_pos, path[0])
                rotation = rotate_to(cast_rot_inverse(moi.direction), rot_req)
                if rotation is None:
                    # if shoot:
                    self.send_message(["move"])
                    # else:
                    #     self.send_message(["move"])
                else:
                    # if shoot:
                    #     self.send_message([rotation])
                    # else:
                    self.send_message([rotation])

        # TODO move to next bonus

    def calc_retourne(self, me, proj):
        (x, y) = proj
        (myx, myy) = me.current_pos()
        if x == myx:
            if y < myy:
                return [0, -1]
            else:
                return [0, 1]
        elif y == myy:
            if x < myx:
                return [-1, 0]
            else:
                return [1, 0]

    def proj_coming(self, proj, me, map):
        (pos, dir) = proj
        (pos, dir) = proj
        (myPos) = me.current_pos()
        x = pos[0]
        y = pos[1]

        while True:
            if x == myPos[0] and y == myPos[1]:
                return (abs(myPos[0] - pos[0]) + abs(myPos[1] - pos[1])) / 2
            if map.get_at(x, y).est_mur():
                return -1
            x += dir[0]
            y += dir[1]

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
        lambda: ClientConcoursProg(loop), args.hostname, args.port
    )

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
