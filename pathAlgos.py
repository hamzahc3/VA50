def heuristic(square1, square2):
    return abs(square1.pos[0] - square2.pos[0]) + abs(square1.pos[1] - square2.pos[1])

import heapq

def a_star(start_square, end_square, grid):
    open_set = []
    heapq.heappush(open_set, (0, start_square))

    # Use square positions as keys
    g_score = {square.pos: float('inf') for row in grid for square in row}
    g_score[start_square.pos] = 0

    f_score = {square.pos: float('inf') for row in grid for square in row}
    f_score[start_square.pos] = heuristic(start_square, end_square)

    came_from = {}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end_square:
            path = []
            while current.pos in came_from:
                path.append(current)
                current = came_from[current.pos]
            return path[::-1]

        neighbors = get_neighbors(current, grid)
        for neighbor in neighbors:
            if not neighbor.free:
                continue

            tentative_g_score = g_score[current.pos] + 1

            if tentative_g_score < g_score[neighbor.pos]:
                came_from[neighbor.pos] = current
                g_score[neighbor.pos] = tentative_g_score
                f_score[neighbor.pos] = tentative_g_score + heuristic(neighbor, end_square)
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor.pos], neighbor))

    return []

def get_neighbors(square, grid):
    x, y = square.pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neighbors.append(grid[nx][ny])
    return neighbors



