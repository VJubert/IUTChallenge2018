from joueur import Joueur


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

        xs = {c['pos'][0] for c in json['map']}
        ys = {c['pos'][1] for c in json['map']}
        self.bornes = [max(xs), max(ys)]

        for j in json['joueurs']:
            xj, yj = j['position']
            self.get_at(xj, yj).set_joueur(
                Joueur(j['id'], j['position'], j['direction']))

    def get_at(self, x, y):
        return self.cells[x + y * (self.bornes[1] + 1)]
