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

    def calc_next_move(self, goal):
        (curx, cury) = tuple(self.current_pos)
        (goalx, goaly) = tuple(goal)
        (dirx, diry) = tuple(self.dir)
        print((curx, cury), (dirx, diry), (goalx, goaly))
        if (curx + dirx) == goalx and (cury + diry) == goaly:
            return "move"
        else:
            goaldirx = goalx - curx
            goaldiry = goaly - cury
            rot_ord = calc_orientation((dirx, diry), (goaldirx, goaldiry))
            print(rot_ord)
            return rot_ord


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

    def is_destructible_wall(self, pos):
        (x, y) = tuple(pos)
        return self.map[x][y] == "C"

    def is_indestrutible_wall(self, pos):
        (x, y) = tuple(pos)
        return self.map[x][y] == "I"

    def is_not_wall(self, pos):
        (x, y) = tuple(pos)
        return self.map[x][y] == " "

    def is_wall(self, pos):
        return not self.is_not_wall(pos)

    def print(self):
        print((self.maxx, self.maxy))
        print(self.map)

    def get_neighbors(self, pos):
        (x, y) = pos
        neigh = []
        if not self.is_indestrutible_wall([x - 1, y]):
            neigh.append((x - 1, y))
        if not self.is_indestrutible_wall([x + 1, y]):
            neigh.append((x + 1, y))
        if not self.is_indestrutible_wall([x, y - 1]):
            neigh.append((x, y - 1))
        if not self.is_indestrutible_wall([x, y + 1]):
            neigh.append((x, y + 1))
        return neigh


class Game:
    my_id = 0
    joueurs = {}
    map = None
    bonus = []
    proj = {}
    cible = None

    def del_bonus(self, posbonus):

        if self.cible is not None:
            (_, cible_pos) = self.cible
            if posbonus == cible_pos:
                self.cible = None

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

    def proj_incoming(self, my_pos, pos, dir) -> int:
        (myx, myy) = tuple(my_pos)
        (posx, posy) = tuple(pos)
        (dirx, diry) = tuple(dir)
        newx = posx
        newy = posy
        while True:
            newx += dirx
            newy += diry
            if newx == myx and newy == myy:
                return abs(posx - myx) + abs(posy - myy)
            if self.map.is_wall([newx, newy]):
                break
        return -1

    def play(self, donnees):
        print("         NEW TURN            ")
        # print(donnees)
        if "idJoueur" in donnees:
            self.my_id = donnees["idJoueur"]
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
                        print("update dir", dir)
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
            my_player = self.joueurs[self.my_id]
            # dest = None
            if len(self.bonus) > 0:
                self.bonus.sort(key=lambda x: a_star(self.map, my_player.current_pos, x[1]), reverse=True)
                (points, pos_bonus) = self.bonus[0]
                path = a_star(self.map, my_player.current_pos, pos_bonus)
                if self.cible is None:
                    self.cible = self.bonus[0]
                else:
                    (cible_points, cible_pos) = self.cible
                    path_cible = a_star(self.map, my_player.current_pos, cible_pos)
                    if (len(path) + 2) < len(path_cible):
                        self.cible = self.bonus
                    else:
                        path = path_cible

                return [my_player.calc_next_move(path[1])]
            else:
                return []


from queue import PriorityQueue


def a_star(graph, start, goal):
    start, goal = tuple(start), tuple(goal)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.get_neighbors(current):
            new_cost = cost_so_far[current] + 1

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + 1
                frontier.put(next, priority)
                came_from[next] = current

    path = []
    current = goal
    while current is not None:
        path.insert(0, current)
        current = came_from[current]
    return path


def calc_orientation(cur_dir, goal_dir):
    print(cur_dir, goal_dir)
    hrot = "hrotate"
    trot = "trotate"
    if cur_dir == (0, 1):
        if goal_dir == (1, 0):
            return hrot
        elif goal_dir == (-1, 0):
            return trot
        elif goal_dir == (0, -1):
            return hrot
    elif cur_dir == (0, -1):
        if goal_dir == (1, 0):
            return hrot
        elif goal_dir == (-1, 0):
            return trot
        elif goal_dir == (0, 1):
            return hrot
    elif cur_dir == (1, 0):
        if goal_dir == (0, 1):
            return trot
        elif goal_dir == (0, -1):
            return hrot
        elif goal_dir == (-1, 0):
            return hrot
    elif cur_dir == (-1, 0):
        if goal_dir == (0, 1):
            return trot
        elif goal_dir == (0, -1):
            return hrot
        elif goal_dir == (1, 0):
            return hrot
    print("WARNING : invalid calc_orientation")
    return
