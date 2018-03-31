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
        self.direction = self.cast_rot(rot)

    def __init__(self, id):
        self.id = id

    def update(self, position, direction):
        self.positions.insert(0, tuple(position))
        self.direction = self.cast_rot(direction)

    def is_safe(self):
        False

    def cast_rot(self, rot):
        if rot == [0, 1]:
            return 3
        elif rot == [0, -1]:
            return 1
        elif rot == [1, 0]:
            return 2
        elif rot == [-1, 0]:
            return 0
