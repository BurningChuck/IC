import math
from typing import Optional

_food_x: Optional[int] = None
_food_y: Optional[int] = None


def g(x, y):
    return math.sqrt(x ** 2 + y ** 2)


def h(x, y):
    global _food_x
    global _food_y
    return math.sqrt((_food_x - x) ** 2 + (_food_y - y) ** 2)


def a_star(maze, measure: bool = False):
    global _food_x
    global _food_y
    _food_x = maze.foodX
    _food_y = maze.foodY

    # [cell, cost], cost = h + f -> min
    path = [[maze[0, 0], h(0, 0)]]
    path[0][0].cost = 0
    maze[0, 0].visited = True
    steps = 0

    while True:
        steps += 1
        if not measure:
            maze.print_maze()

        path = sorted(path, key=lambda x: x[1], reverse=True)
        found = False
        item = path.pop()[0]

        for new_item in maze.connected_neighbors(item):
            if new_item.visited and new_item.cost > item.cost + 1:
                new_item.previous = item
                new_item.cost = item.cost + 1
                continue
            elif new_item.visited and new_item.cost <= item.cost + 1:
                continue
            elif new_item.isFood:
                found = True
                new_item.previous = item
                path.append(new_item)
                break
            new_item.previous = item
            new_item.cost = item.cost + 1
            new_item.visited = True
            path.append([new_item, g(new_item.x, new_item.y) + h(new_item.x, new_item.y)])

        if found:
            path_final = [path.pop()]
            while True:
                path_final.append(path_final[-1].previous)
                if path_final[-1].previous is None:
                    break
            return path_final[::-1], steps
