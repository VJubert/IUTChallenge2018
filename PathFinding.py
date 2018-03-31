from queue import PriorityQueue


def aStar(graph, start, goal):
    start, goal = tuple(start), tuple(goal)
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
