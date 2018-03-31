def cast_rot(rot):
    if rot == [0, 1]:
        return 3
    elif rot == [0, -1]:
        return 1
    elif rot == [1, 0]:
        return 2
    elif rot == [-1, 0]:
        return 0


def cast_rot_inverse(rot):
    if rot == 0:
        return [-1, 0]
    elif rot == 1:
        return [0, -1]
    elif rot == 2:
        return [1, 0]
    elif rot == 3:
        return [0, 1]


class Joueur:
    # pile des positions (0 is top)
    positions = []
    # 0 nord / 1 est / 2 sud / 3 ouest
    direction = 0
    id = 0
    score = 0

    def current_pos(self):
        return self.positions[0]

    def __init__(self, id, pos, rot):
        self.id = id
        if not pos is None:
            self.positions.insert(0, pos)
            self.direction = cast_rot(rot)

    def update(self, position, direction):
        self.positions.insert(0, tuple(position))
        self.direction = cast_rot(direction)

    def update_dir(self, direction):
        self.direction = cast_rot(direction)

    def update_pos(self, pos):
        self.positions.insert(0, tuple(pos))

    def __str__(self) -> str:
        return self.id + " " + self.positions[0]
