import os
import random
from time import sleep
from numpy import reshape

N, S, W, E = ('n', 's', 'w', 'e')


class Cell(object):
    """
    Class for each cell. Knows its position and which walls are standing.
    """

    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)
        self.visited = False
        self.isFood = False
        self.previous = None  # For bfs and a*
        self.cost = 1000000000

    def __repr__(self):
        # <15, 25 (es  )>
        return '<{}, {} ({:4})>'.format(self.x, self.y, ''.join(sorted(self.walls)))

    def __contains__(self, item):
        # N in cell
        return item in self.walls

    def is_full(self):
        """
        Returns True if all walls are standing.
        """
        return len(self.walls) == 4

    def wall_to(self, other):
        """
        Returns the direction to the given cell from the current one.
        Must be one cell away only.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, '{}, {}'.format(self, other)
        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E
        else:
            assert False

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        other.walls.remove(other.wall_to(self))
        self.walls.remove(self.wall_to(other))


class Maze(object):
    """
    Maze class containing full board and maze generation algorithms.
    """

    UNICODE_BY_CONNECTIONS = {'ensw': '┼',
                              'ens': '├',
                              'enw': '┴',
                              'esw': '┬',
                              'es': '┌',
                              'en': '└',
                              'ew': '─',
                              'e': '╶',
                              'nsw': '┤',
                              'ns': '│',
                              'nw': '┘',
                              'sw': '┐',
                              's': '╷',
                              'n': '╵',
                              'w': '╴'}

    def __init__(self, width=20, height=20):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.width = width
        self.height = height
        self.cells = []
        self.foodX = 0
        self.foodY = 0
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, E, W]))

    def __getitem__(self, index):
        """
        Returns the cell at index (x, y).
        """
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells, without diagonals.
        """
        x = cell.x
        y = cell.y
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[new_x, new_y]
            if neighbor is not None:
                yield neighbor

    def connected_neighbors(self, cell):
        """
        Returns the list of neighboring cells, that are connected with the current one.
        """
        x = cell.x
        y = cell.y
        res = []

        if N not in cell.walls:
            res.append(self[x, y-1])
        if S not in cell.walls:
            res.append(self[x, y+1])
        if W not in cell.walls:
            res.append(self[x-1, y])
        if E not in cell.walls:
            res.append(self[x+1, y])

        return res

    def _to_str_matrix(self):
        """
        Returns a matrix with a visual representation of the maze.
        """
        str_matrix = [['O'] * (self.width * 2 + 1)
                      for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1

            if cell.isFood:
                str_matrix[y][x] = '@'
            elif cell.visited:
                str_matrix[y][x] = 'o'
            else:
                str_matrix[y][x] = ' '

            if N not in cell and y > 0:
                str_matrix[y - 1][x] = ' '
            if S not in cell and y + 1 < self.width:
                str_matrix[y + 1][x] = ' '
            if W not in cell and x > 0:
                str_matrix[y][x - 1] = ' '
            if E not in cell and x + 1 < self.width:
                str_matrix[y][x + 1] = ' '

        return str_matrix

    def __repr__(self):
        """
        Returns an Unicode representation of the maze. Size is doubled
        horizontally to avoid a stretched look.
        """
        skinny_matrix = self._to_str_matrix()

        # Duplicate each character in each line to stretch horizontally
        double_wide_matrix = []
        for line in skinny_matrix:
            double_wide_matrix.append([])
            for char in line:
                double_wide_matrix[-1].append(char)
                double_wide_matrix[-1].append(' ' if char in ('@', 'o') else char)

        # Remove the last char of each line because they are walls
        matrix = [line[:-1] for line in double_wide_matrix]

        def g(x, y):
            """
            Returns True if there is a wall at (x, y). Values outside the valid
            range always return false.
            """
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix):
                return matrix[y][x] not in (' ', '@', 'o')
            else:
                return False

        # Fix double wide walls
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y) and g(x - 1, y):
                    matrix[y][x - 1] = ' '

        # Replacing the walls with Unicode characters
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y):
                    continue

                connections = {N, S, E, W}
                if not g(x, y + 1):
                    connections.remove(S)
                if not g(x, y - 1):
                    connections.remove(N)
                if not g(x + 1, y):
                    connections.remove(E)
                if not g(x - 1, y):
                    connections.remove(W)

                str_connections = ''.join(sorted(connections))
                matrix[y][x] = Maze.UNICODE_BY_CONNECTIONS[str_connections]

        return '\n'.join(''.join(line) for line in matrix) + '\n'

    def print_maze(self):
        os.system("cls")
        print(self)
        sleep(0.01)

    def randomize(self, measure: bool = False):
        """
        Destroys random walls to build a random maze.
        """
        cell_stack = []
        cell = random.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            if not measure:
                self.print_maze()

            neighbors = [c for c in self.neighbors(cell) if c.is_full()]
            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

    def generateFood(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        self[x, y].isFood = True
        self.foodX = x
        self.foodY = y

    def get_cells(self):
        return reshape(self.cells, (self.width, self.height)).tolist()

    def _reset(self):
        for cell in self.cells:
            cell.visited = False

    def show_path(self, path):
        self._reset()
        for item in path:
            x, y = item.x, item.y
            self[x, y].visited = True
            self.print_maze()
            self[x, y].visited = False
        self.print_maze()

    @staticmethod
    def generate(width=10, height=10, measure: bool = False):
        """
        Returns a new random maze with given sizes.
        """
        m = Maze(width, height)
        m.randomize(measure)
        return m
