from queue import PriorityQueue

import Map


# def aStar(map, start, goal):
#     print("fsqyf")
#     queue = [start]
#     cost = {start: 0}
#     prec = {start: None}
#     priority = {start: 0}
#
#     while len(queue) > 0:
#         print(len(queue))
#         (x, y) = queue.pop(0)
#         if (x, y) == goal:
#             print("goal")
#             break
#         for (nl, nc) in map.get_neighbors(x, y):
#             print(nl, " ", nc, " ", x, " ", y)
#             newCost = cost[(x, y)] + 1
#             if not (nl, nc) in cost or cost[(nl, nc)] < newCost:
#                 cost[(nl, nc)] = newCost
#                 queue.append((nl, nc))
#                 prec[(nl, nc)] = (x, y)
#                 priority[(nl, nc)] = newCost + 1
#         comparer = lambda x: priority[x]
#         queue.sort(key=comparer)
#
#     path = []
#     current = goal
#     while current is not None:
#         path.insert(0, current)
#         current = prec[current]
#     print(path)
#     return path


def aStar(graph, start, goal):
    if start == goal:
        return []


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

        for next in graph.get_neighbors(current[0], current[1]):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + 1
                frontier.put(next, priority)
                came_from[next] = current

    path = []
    current = goal
    while current is not None:
        # path.insert(0, current)
        path.append(current)
        current = came_from[current]
    # print(path)
    return path
