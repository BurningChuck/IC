def bfs(maze, measure: bool = False):
    path = []
    items = [maze[0, 0]]
    items[0].visited = True

    found = False
    steps = 0

    while len(items) > 0:
        if not measure:
            maze.print_maze()

        new_items = []
        for item in items:
            for i in maze.connected_neighbors(item):
                if i.visited:
                    continue
                if i.isFood:
                    found = True
                    i.previous = item
                    path = [i]
                    break
                i.visited = True
                i.previous = item
                steps += 1
                new_items.append(i)

        items = new_items

        if found:
            break

    while True:
        if path[-1].previous:
            path.append(path[-1].previous)
        else:
            break

    return path[::-1], steps
