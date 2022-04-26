from dataclasses import dataclass, field
from random import randint, choice
from time import sleep
from typing import List
import os


@dataclass
class MazeItem:
    id: int
    i: int
    j: int

    is_wall: bool = None
    is_visited: bool = False
    is_food: bool = False
    connected: List["MazeItem"] = field(default_factory=list)
    prev_item: "MazeItem" = None  # for bfs

    def __str__(self):
        # return f"\033[92mX \033[0m" if self.is_wall else "  "
        return f"\033[92m" + u"\u25A0" + f" \033[0m" if self.is_wall else "  "
        # return u"\u25A0" + " " if self.is_wall else "  "

    @property
    def path_search_style(self) -> str:
        if self.is_visited:
            return "o "
        if self.is_food:
            return "Y "
        return str(self)

    def path_visualisation_style(self, i, j):
        if self.i == i and self.j == j:
            return "o "
        if self.is_food:
            return "Y "
        return str(self)


_map: List[List[MazeItem]]
_term: bool
_measure: bool


def print_maze():
    global _map

    print("-" * (len(_map) * 2 + 2))
    for row in _map:
        print("|" + "".join([str(item) for item in row]) + "|")
    print("-" * (len(_map) * 2 + 2))


def generate_maze(n: int, term: bool = False, measure: bool = False):
    global _map
    global _term
    global _measure

    _term = term
    _measure = measure
    _map = [[MazeItem(n * i + j, i=i, j=j) for j in range(n)] for i in range(n)]

    _divide(0, 0, n - 1, n - 1, True)

    if not _term:
        print_maze()

    return _map


def _divide(i1, j1, i2, j2, vertical: bool):
    global _map
    global _term
    global _measure

    if _term and not _measure:
        os.system("cls")
        print_maze()
        sleep(0.02)

    # edge case when need to divide 2/2, bottom of recursion
    if abs(i1 - i2) == 1:
        items = [
            _map[i1][j1],
            _map[i1][j2],
            _map[i2][j1],
            _map[i2][j2],
        ]
        # items that are not marked as wall or not wall
        free_items = [item for item in items if item.is_wall is None]
        if len(free_items) == 0:
            # connecting that items
            for item in items:
                if item.i == i2:
                    i_ = item.i - 1
                else:
                    i_ = item.i + 1
                if item.j == j2:
                    j_ = item.j - 1
                else:
                    j_ = item.j + 1
                if not _map[item.i][j_] in item.connected:
                    item.connected.append(_map[item.i][j_])
                if not _map[i_][item.j] in item.connected:
                    item.connected.append(_map[i_][item.j])
            return
        # random select a wall
        wall = choice(free_items)
        wall.is_wall = True
        free_items.remove(wall)

        for item in free_items:
            item.is_wall = False

        # connecting items
        if wall.i == i2:
            i = wall.i - 1
        else:
            i = wall.i + 1
        if wall.j == j2:
            j = wall.j - 1
        else:
            j = wall.j + 1
        _map[i][j].connected.append(_map[i][wall.j])
        _map[i][j].connected.append(_map[wall.i][j])
        _map[i][wall.j].connected.append(_map[i][j])
        _map[wall.i][j].connected.append(_map[i][j])

        return

    # two types of dividing
    if vertical:
        i = randint(i1, i2)
        # will block the path later, move to +1
        if i == abs(i1 + i2) // 2:
            i += 1
        j = (j1 + j2) // 2

        connected = [[i, j - 1], [i, j], [i, j + 1]]
        wall = [[i_, j] for i_ in range(i1, i2 + 1) if not i_ == i]
    else:
        i = (i1 + i2) // 2
        j = randint(j1, j2)
        # will block the path later, move to +1
        if j == abs(j1 + j2) // 2:
            j += 1

        connected = [[i - 1, j], [i, j], [i + 1, j]]
        wall = [[i, j_] for j_ in range(j1, j2 + 1) if not j_ == j]

    for item in wall:
        # if we marked that this can't we a wall
        if _map[item[0]][item[1]].is_wall is False:
            # connecting items
            if item[0] < len(_map) + 1:
                if _map[item[0] + 1][item[1]] not in _map[item[0]][item[1]].connected:
                    _map[item[0]][item[1]].connected.append(_map[item[0] + 1][item[1]])
                if _map[item[0]][item[1]] not in _map[item[0] + 1][item[1]].connected:
                    _map[item[0] + 1][item[1]].connected.append(_map[item[0]][item[1]])
            if item[0] > 0:
                if _map[item[0] - 1][item[1]] not in _map[item[0]][item[1]].connected:
                    _map[item[0]][item[1]].connected.append(_map[item[0] - 1][item[1]])
                if _map[item[0]][item[1]] not in _map[item[0] - 1][item[1]].connected:
                    _map[item[0] - 1][item[1]].connected.append(_map[item[0]][item[1]])
            if item[1] < len(_map) + 1:
                if _map[item[0]][item[1] + 1] not in _map[item[0]][item[1]].connected:
                    _map[item[0]][item[1]].connected.append(_map[item[0]][item[1] + 1])
                if _map[item[0]][item[1]] not in _map[item[0]][item[1] + 1].connected:
                    _map[item[0]][item[1] + 1].connected.append(_map[item[0]][item[1]])
            if item[1] > 0:
                if _map[item[0]][item[1] - 1] not in _map[item[0]][item[1]].connected:
                    _map[item[0]][item[1]].connected.append(_map[item[0]][item[1] - 1])
                if _map[item[0]][item[1]] not in _map[item[0]][item[1] - 1].connected:
                    _map[item[0]][item[1] - 1].connected.append(_map[item[0]][item[1]])
            continue
        _map[item[0]][item[1]].is_wall = True

    # connecting items near path
    _map[connected[0][0]][connected[0][1]].connected.append(
        _map[connected[1][0]][connected[1][1]]
    )
    _map[connected[1][0]][connected[1][1]].connected.append(
        _map[connected[0][0]][connected[0][1]]
    )
    _map[connected[1][0]][connected[1][1]].connected.append(
        _map[connected[2][0]][connected[2][1]]
    )
    _map[connected[2][0]][connected[2][1]].connected.append(
        _map[connected[1][0]][connected[1][1]]
    )

    for item in connected:
        _map[item[0]][item[1]].is_wall = False

    # recursion
    if vertical:
        _divide(i1, j1, i2, j - 1, not vertical)
        _divide(i1, j + 1, i2, j2, not vertical)
    else:
        _divide(i1, j1, i - 1, j2, not vertical)
        _divide(i + 1, j1, i2, j2, not vertical)
