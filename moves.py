def cost_orientation(src, dest):
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
    if cost == 0:
        return None
    elif cost > 0:
        return "trotate"
    else:
        return "hrotate"
