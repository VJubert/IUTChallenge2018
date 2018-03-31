from joueur import *


class Cell:
    def __init__(self, data):
        self.x, self.y = data['pos']

        self.cassable = None
        self.points = None

        if 'cassable' in data:
            self.cassable = data['cassable']
        if 'points' in data:
            self.points = data['points']

        self.joueur = None

    def set_joueur(self, joueur):
        self.joueur = joueur

    def joueur_present(self):
        return self.joueur is not None

    def est_bonus(self):
        return self.points is not None


class Map:
    def __init__(self, json):
        self.cells = [Cell(x) for x in json['map']]
        self.joueurs = []

        xs = {c['pos'][0] for c in json['map']}
        ys = {c['pos'][1] for c in json['map']}
        self.bornes = [max(xs), max(ys)]

        for j in json['joueurs']:
            xj, yj = j['position']
            J = Joueur(j['id'], j['position'], j['direction'])
            self.get_at(xj, yj).set_joueur(J)
            self.joueurs.append(J)

    def get_at(self, x, y):
        return self.cells[x + y * (self.bornes[1] + 1)]

    def get_neighbors(self,(x, y)):
        n = []
        if x-1>=0:
            n.append((x-1,y))
        if x+1<=self.bornes[0]:
            n.append((x+1,y))
        if y-1>=0:
            n.append((x,y-1))
        if y+1<=self.bornes[1]:
            n.append((x,y+1))

    def get_joueur(self, id):
        for j in self.joueurs:
            if j.id == id:
                return j
        return None

    def move_joueur(self, id):
        j = self.get_joueur(id)
        dir = cast_rot_inverse(j.direction)
        pos = j.positions[0]
        dest = [pos[i] + dir[i] for i in range(len(pos))]

        from_cell = self.get_at(*pos)
        dest_cell = self.get_at(*dest)

        from_cell.set_joueur(None)
        dest_cell.set_joueur(j)
        j.update_pos(tuple(dest))

    def rotate_joueur(self, id, dir):
        j = self.get_joueur(id)
        j.update_dir(cast_rot(dir))

    def add_bonus(self, id, pos_bonus):
        j = self.get_joueur(id)
        cell = self.get_at(*pos_bonus)

        j.score += cell.points
        cell.points = None

    def update(self, events):
        for e in events:
            what = e[0]
            typ = e[1]

            if what == 'joueur':
                id = e[2]
                if typ == 'move':
                    self.move_joueur(id)
                elif typ == 'rotate':
                    self.rotate_joueur(id, e[3])
                elif typ == 'recupere_bonus':
                    self.add_bonus(id, e[3])
                elif typ == 'shoot':
                    pass
                elif typ == 'respawn':
                    pass
            elif what == 'projectile':
                if typ == 'move':
                    pass
                elif typ == 'explode':
                    pass
>>>>>>> 1e35e0b6ffa2c67d42e115df508b7f27de4cb007
