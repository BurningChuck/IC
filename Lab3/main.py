import sys
import os
import psutil
from time import time
from maze import Maze
from bfs import bfs
from dfs import dfs
from a_star import a_star
from greedy import greedy


def _process_argv():
    args = {
        "algo": None,
        "width": 10,
        "height": 10,
        "measure": False,
    }
    for arg in sys.argv:
        if arg == "--measure":
            args["measure"] = True
        if arg.startswith("algo"):
            args["algo"] = arg.split("=")[1]
        if arg.startswith("width"):
            args["width"] = int(arg.split("=")[1])
        if arg.startswith("height"):
            args["height"] = int(arg.split("=")[1])

    if args["algo"] == "bfs":
        args["algo"] = bfs
    elif args["algo"] == "dfs":
        args["algo"] = dfs
    elif args["algo"] == "a_star":
        args["algo"] = a_star
    else:
        args["algo"] = greedy

    for arg in args.values():
        assert arg is not None

    return args


if __name__ == '__main__':
    args = _process_argv()

    t1 = time()
    maze = Maze.generate(args["width"], args["height"], args["measure"])
    maze.generateFood()
    t2 = time()
    maze_generation_time = t2 - t1

    maze.print_maze()

    cells = maze.get_cells()
    t1 = time()
    path, steps = args["algo"](maze, args["measure"])
    t2 = time()
    path_search_time = t2 - t1

    maze.show_path(path)

    if args["measure"]:
        print(f"Maze generation: {maze_generation_time} s.")
        print(f"Path search: {path_search_time} s.")
        print(f"Algorithm steps: {steps}")
        print(f"Path length: {len(path)}")
        process = psutil.Process(os.getpid())
        print(f"Memory used: {process.memory_info().rss / 1024 ** 2} mb.")
