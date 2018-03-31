class Joueur:
    # pile des positions
    positions = []
    # 0 nord / 1 est / 2 sud / 3 ouest
    direction = 0
    id = 0
    score = 0

    def __init__(self, id, pos, rot):
        self.id = id
        self.positions.insert(0, pos)
        if rot == [0, 1]:
            self.direction = 3
        elif rot == [0, -1]:
            self.direction = 1
        elif rot == [1, 0]:
            self.direction = 2
        elif rot == [-1, 0]:
            self.direction = 0

    def __init__(self, id):
        self.id = id

    def update(self, position):
        self.positions.insert(0, position)

    def is_safe(self):
        False
