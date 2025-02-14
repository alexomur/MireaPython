# 48.36
import heapq


def dijkstra_astar(check, start, goal):
    """A* + Dijkstra для поиска пути от start до goal"""
    x0, y0 = start
    gx, gy = goal
    queue = [(0, x0, y0, [])]  # (стоимость, x, y, путь)
    visited = {}

    while queue:
        cost, x, y, path = heapq.heappop(queue)
        if (x, y) in visited and visited[(x, y)] <= cost:
            continue
        visited[(x, y)] = cost

        if (x, y) == goal:
            return path[0] if path else "pass"

        for dx, dy, move in [
            (-1, 0, "left"),
            (1, 0, "right"),
            (0, -1, "up"),
            (0, 1, "down"),
        ]:
            nx, ny = x + dx, y + dy
            if check("wall", nx, ny):
                continue
            g = cost + 1
            h = abs(nx - gx) + abs(ny - gy)  # Манхэттенская эвристика
            heapq.heappush(queue, (g + h, nx, ny, path + [move]))

    return "pass"


def script(check, x, y):
    """Логика бота"""
    if check("gold", x, y):
        return "take"

    # Собираем позиции золота
    gold_positions = {
        (gx, gy) for gx in range(32) for gy in range(32) if check("gold", gx, gy)
    }

    if gold_positions:
        # Ищем ближайшее золото
        goal = min(gold_positions, key=lambda pos: abs(pos[0] - x) + abs(pos[1] - y))
        return dijkstra_astar(check, (x, y), goal)

    return "right" if not check("wall", x + 1, y) else "down"

# 45.8
# import heapq
#
#
# def astar(check, start, goals):
#     """A* поиск пути от start до ближайшей цели из goals."""
#     x0, y0 = start
#     queue = []
#     heapq.heappush(queue, (0, x0, y0, []))
#     visited = set()
#
#     while queue:
#         f, x, y, path = heapq.heappop(queue)
#         if (x, y) in visited:
#             continue
#         visited.add((x, y))
#
#         if (x, y) in goals:
#             return path[0] if path else "pass"
#
#         for dx, dy, move in [
#             (-1, 0, "left"),
#             (1, 0, "right"),
#             (0, -1, "up"),
#             (0, 1, "down"),
#         ]:
#             nx, ny = x + dx, y + dy
#             if check("wall", nx, ny) or (nx, ny) in visited:
#                 continue
#             g = len(path) + 1
#             h = min(abs(nx - gx) + abs(ny - gy) for gx, gy in goals)
#             heapq.heappush(queue, (g + h, nx, ny, path + [move]))
#
#     return "pass"
#
#
# def script(check, x, y):
#     if check("gold", x, y):
#         return "take"
#     gold_positions = [
#         (gx, gy) for gx in range(32) for gy in range(32) if check("gold", gx, gy)
#     ]
#     if gold_positions:
#         return astar(check, (x, y), gold_positions)
#     return "right" if not check("wall", x + 1, y) else "down"
#

# 48.7
# import heapq
#
#
# def astar(check, start, goal):
#     """A* поиск пути от start до goal."""
#     x0, y0 = start
#     gx, gy = goal
#     queue = [(0, x0, y0, [])]  # (f, x, y, path)
#     visited = set()
#
#     while queue:
#         f, x, y, path = heapq.heappop(queue)
#         if (x, y) in visited:
#             continue
#         visited.add((x, y))
#
#         if (x, y) == goal:
#             return path[0] if path else "pass"
#
#         for dx, dy, move in [
#             (-1, 0, "left"),
#             (1, 0, "right"),
#             (0, -1, "up"),
#             (0, 1, "down"),
#         ]:
#             nx, ny = x + dx, y + dy
#             if check("wall", nx, ny) or (nx, ny) in visited:
#                 continue
#             g = len(path) + 1
#             h = abs(nx - gx) + abs(ny - gy)  # Манхэттенское расстояние
#             heapq.heappush(queue, (g + h, nx, ny, path + [move]))
#
#     return "pass"
#
#
# def script(check, x, y):
#     """Логика бота"""
#     if check("gold", x, y):
#         return "take"
#
#     # Собираем позиции золота в множество для быстрого поиска
#     gold_positions = {
#         (gx, gy) for gx in range(32) for gy in range(32) if check("gold", gx, gy)
#     }
#
#     # Если есть золото, ищем путь к ближайшему
#     if gold_positions:
#         goal = min(gold_positions, key=lambda pos: abs(pos[0] - x) + abs(pos[1] - y))
#         return astar(check, (x, y), goal)
#
#     # Если золота нет, просто идём вправо или вниз
#     return "right" if not check("wall", x + 1, y) else "down"

# 48.6
# import heapq
#
#
# def astar(check, start, goal):
#     """Находит путь от start до goal с A*."""
#     x0, y0 = start
#     gx, gy = goal
#     queue = [(0, x0, y0, [])]  # (стоимость, x, y, путь)
#     visited = set()
#
#     while queue:
#         cost, x, y, path = heapq.heappop(queue)
#         if (x, y) in visited:
#             continue
#         visited.add((x, y))
#
#         if (x, y) == goal:
#             return path
#
#         for dx, dy, move in [
#             (-1, 0, "left"),
#             (1, 0, "right"),
#             (0, -1, "up"),
#             (0, 1, "down"),
#         ]:
#             nx, ny = x + dx, y + dy
#             if check("wall", nx, ny):
#                 continue
#             heapq.heappush(
#                 queue, (cost + 1 + abs(nx - gx) + abs(ny - gy), nx, ny, path + [move])
#             )
#
#     return []  # Если пути нет
#
#
# def find_nearest_gold(check, x, y, gold_positions):
#     """Находит ближайшую точку золота."""
#     closest_gold = None
#     min_distance = float("inf")
#
#     for gx, gy in gold_positions:
#         path = astar(check, (x, y), (gx, gy))
#         if path and len(path) < min_distance:
#             closest_gold = (gx, gy)
#             min_distance = len(path)
#
#     return closest_gold
#
#
# def script(check, x, y):
#     """Логика бота: собираем золото по ближайшему пути."""
#     if check("gold", x, y):
#         return "take"
#
#     gold_positions = {
#         (gx, gy) for gx in range(32) for gy in range(32) if check("gold", gx, gy)
#     }
#
#     while gold_positions:
#         closest_gold = find_nearest_gold(check, x, y, gold_positions)
#         if closest_gold:
#             move_path = astar(check, (x, y), closest_gold)
#             if move_path:
#                 next_move = move_path[0]
#                 x, y = x + (
#                     1 if next_move == "right" else -1 if next_move == "left" else 0
#                 ), y + (1 if next_move == "down" else -1 if next_move == "up" else 0)
#                 gold_positions.remove(closest_gold)
#                 return next_move
#         else:
#             break  # No more gold, stop
#
#     return "right" if not check("wall", x + 1, y) else "down"
