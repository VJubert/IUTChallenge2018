import Map


def aStar(self, map, start, goal):
    queue = [start]
    cost = {start: 0}
    prec = {start: None}
    priority = {start: 0}

    while len(queue) > 0:
        (x, y) = queue.pop(0)
        if x == goal[0] and y == goal[0]:
            break
        for (nl, nc) in map.get_neighbors((x, y)):
            newCost = cost[(x, y)] + 1
            if not (nl, nc) in cost or cost[(nl, nc)] < newCost:
                cost[(nl, nc)] = newCost
                queue.append((nl, nc))
                prec[(nl, nc)] = (x, y)
                priority[(nl, nc)] = newCost + 1
        comparer = lambda x: priority[x]
        queue.sort(key=comparer)

    path = []
    current = goal
    while current is not None:
        path.insert(0, current)
        current = prec[current]
    print(path)
    return path
