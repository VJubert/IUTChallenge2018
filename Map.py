from joueur import *


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y

        self.cassable = None
        self.points = None
        self.joueur = None

    def set_joueur(self, joueur):
        self.joueur = joueur

    def joueur_present(self):
        return self.joueur is not None

    def est_bonus(self):
        return self.points is not None

    def est_mur(self):
        return self.cassable is not None


class Map:
    def __init__(self, json):
        self.joueurs = []

        # xs = {c['pos'][0] for c in json['map']}
        # ys = {c['pos'][1] for c in json['map']}
        # self.bornes = [max(xs), max(ys)]

        self.bornes = json['map'][-1]['pos']
        self.cells = [Cell(i % self.bornes[1], i // self.bornes[1])
                      for i in range((self.bornes[0] + 1) * (self.bornes[1] + 1))]
        self.cells.sort(key=lambda c: (c.x, c.y))

        for j in json['joueurs']:
            xj, yj = j['position']
            J = Joueur(j['id'], j['position'], j['direction'])

            cell = self.get_at(xj, yj)
            cell.set_joueur(J)
            self.joueurs.append(J)

        for d in json['map']:
            cell = self.get_at(*d['pos'])
            cell.points = d.get('points', None)
            cell.cassable = d.get('cassable', None)

    def get_at(self, x, y):
        cell = self.cells[y + x * (self.bornes[1] + 1)]
        return cell

    def get_neighbors(self, x, y):
        n = []
        if x - 1 >= 0 and not self.get_at(x - 1, y).est_mur():
            n.append((x - 1, y))
        if x + 1 <= self.bornes[0] and not self.get_at(x + 1, y).est_mur():
            n.append((x + 1, y))
        if y - 1 >= 0 and not self.get_at(x, y - 1).est_mur():
            n.append((x, y - 1))
        if y + 1 <= self.bornes[1] and not self.get_at(x, y + 1).est_mur():
            n.append((x, y + 1))
        return n;

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
        j.update_dir(dir)

    def add_bonus(self, id, pos_bonus):
        j = self.get_joueur(id)
        cell = self.get_at(*pos_bonus)

        j.score += cell.points
        cell.points = None

    def respawn_joueur(self, id, pos):
        j = self.get_joueur(id)
        j.update_pos(pos)
        cell = self.get_at(*pos)
        cell.set_joueur(j)

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
                    self.respawn_joueur(e[2], e[3])
            elif what == 'projectile':
                if typ == 'move':
                    pass
                elif typ == 'explode':
                    pass
