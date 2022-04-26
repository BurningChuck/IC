def dfs(maze, measure: bool = False):
    x, y = 0, 0
    path = [maze[x, y]]
    path[0].visited = True

    found = False
    steps = 0

    while True:
        if not measure:
            maze.print_maze()

        item = maze[x, y]

        # search where to go from current item
        next_found = False
        for item in maze.connected_neighbors(item):
            if item.isFood:
                found = True
                break
            if not item.visited:
                x, y = item.x, item.y
                next_found = True
                break

        if found:
            break

        if next_found:
            path.append(maze[x, y])
            maze[x, y].visited = True
            x, y = maze[x, y].x, maze[x, y].y
            steps += 1
            continue
        else:
            # didn't found where to go from current item, move back until not visited item found
            while True:
                steps += 1
                found_not_visited = False

                last_item = path[-1]
                for item in maze.connected_neighbors(last_item):
                    if not item.visited:
                        found_not_visited = True
                        break

                if found_not_visited:
                    x, y = last_item.x, last_item.y
                    break
                else:
                    path.pop()
            continue

    return path, steps
