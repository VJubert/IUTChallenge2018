class Joueur:
    id = -1
    current_pos = []
    pos = []
    dir = []

    def __init__(self, id, pos, dir):
        self.id = id
        self.current_pos = pos
        self.pos.insert(0, pos)
        self.dir = dir

    def update_dir(self, dir):
        self.dir = dir

    def update_pos(self, pos):
        self.current_pos = pos
        self.pos.insert(0, pos)

    def dead(self):
        current_pos = []
        pos = []
        dir = []

    def move(self):
        try:
            (curx, cury) = tuple(self.current_pos)
            (dirx, diry) = tuple(self.dir)
            newx = curx + dirx
            newy = cury + diry
            self.update_pos([newx, newy])
        except:
            print("WARNING : try to move before respawn")


class Map:
    walls = []
    map = []
    maxx = 0
    maxy = 0

    def add_wall(self, cassable, pos):
        self.walls.append((cassable, pos))

    def setupMap(self):
        # find max
        for _, pos in self.walls:
            if pos[0] > self.maxx:
                self.maxx = pos[0]
            if pos[1] > self.maxy:
                self.maxy = pos[1]

        for i in range(self.maxx + 1):
            self.map.append([])
            for j in range(self.maxy + 1):
                self.map[i].append(" ")

        for cassable, pos in self.walls:
            x = pos[0]
            y = pos[1]
            if cassable:
                self.map[x][y] = "C"
            else:
                self.map[x][y] = "I"

    def destroy_wall(self, pos):
        (x, y) = tuple(pos)
        if self.map[x][y] == "C":
            self.map[x][y] = " "
        else:
            print("WARNING : can't destroy wall", (x, y))

    def print(self):
        print((self.maxx, self.maxy))
        print(self.map)


class Game:
    myId = 0
    joueurs = {}
    map = None
    bonus = []
    proj = {}

    def del_bonus(self, posbonus):
        to_remove = None
        for (points, pos) in self.bonus:
            if pos == posbonus:
                to_remove = (points, pos)
                break

        if to_remove is not None:
            self.bonus.remove(to_remove)
        else:
            print("WARNING : CANT REMOVE BONUS", posbonus)

    def explode(self, idproj, pos, murPosList, tank_killed):
        del self.proj[idproj]
        if tank_killed:
            # kill tank
            for _, j in self.joueurs.items():
                if j.current_pos == pos:
                    j.dead()
                    break

        # destroy wall
        for pos in murPosList:
            self.map.destroy_wall(pos)

    def play(self, donnees):
        print("         NEW TURN            ")
        # print(donnees)
        if "idJoueur" in donnees:
            myId = donnees["idJoueur"]
        elif "map" in donnees:
            # init map
            self.map = Map()
            for item in donnees["map"]:
                # init mur
                if "cassable" in item:
                    cassable = item["cassable"]
                    pos = item["pos"]
                    self.map.add_wall(cassable, pos)
                # init bonus
                elif "points" in item:
                    points = item["points"]
                    pos = item["pos"]
                    self.bonus.append((points, pos))
            # fin init map
            self.map.setupMap()

            # init joueur
            for j in donnees["joueurs"]:
                id = j["id"]
                pos = j["position"]
                dir = j["direction"]
                self.joueurs[id] = Joueur(id, pos, dir)
        else:
            # update
            for play in donnees:
                action = play[1]
                if "joueur" in play:
                    if action == "move":
                        id = play[2]
                        self.joueurs[id].move()
                    elif action == "rotate":
                        id = play[2]
                        dir = play[3]
                        self.joueurs[id].update_dir(dir)
                    elif action == "recupere_bonus":
                        id = play[2]
                        pos = play[3]
                        self.del_bonus(pos)
                        # ignore score
                    elif action == "shoot":
                        idj = play[2]
                        idp = play[3]
                        pos = play[4]
                        dir = play[5]
                        self.proj[idp] = (idj, pos, dir)
                    elif action == "respawn":
                        id = play[2]
                        pos = play[3]
                        self.joueurs[id].update_pos(pos)
                elif "projectile" in play:
                    if action == "move":
                        id = play[2]
                        pos = play[3]
                        (idj, oldpos, dir) = self.proj[id]
                        self.proj[id] = (idj, pos, dir)
                    elif action == "explode":
                        idp = play[2]
                        pos = play[3]
                        murDone = play[4]
                        tank_killed = play[5]
                        # ignore score
                        self.explode(idp, pos, murDone, tank_killed)
        # jeu
        return ["hrotate", "shoot"]
