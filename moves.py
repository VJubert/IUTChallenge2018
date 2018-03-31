def cost_orientation(src, dest):
    src, dest = tuple(src), tuple(dest)
    if src == dest:
        return 0

    delta_x = src[0] + dest[0]
    delta_y = src[1] + dest[1]
    if delta_x == 0 or delta_y == 0:
        return 2

    xy = src[0] + dest[1]
    if xy >= 0:
        return 1
    else:
        return -1


def rotate_to(src, dest):
    cost = cost_orientation(src, dest)
    # print("cost = ", cost)
    if cost == 0:
        return None
    elif cost > 0:
        return "trotate"
    else:
        return "hrotate"


def rotation_requise(src, dest):
    if dest[0] < src[0]:
        return (-1, 0)
    elif dest[0] > src[0]:
        return(1, 0)
    elif dest[1] < src[1]:
        return (0, -1)
    else:
        return(0, 1)
