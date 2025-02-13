from collections import deque
import random

DEBUG = False

def print(*args, debug=DEBUG):
    if debug:
        print(*args)

def draw_graph(check, x, y, max_distance=None) -> (dict, dict):
    """
    Составляет граф доступных клеток, начиная с позиции (x, y), используя обход в ширину (BFS).
    Если параметр max_distance=None, то поиск идёт по всему достижимому компоненту связности.

    Возвращает два словаря:
      - graph: ключ – координата (x, y), значение – список соседних координат (без стен)
      - coins: ключ – координата, значение – количество монеток на клетке (да, согласно логике игры, их может быть несколько)
    """
    graph = {}
    coins = {}
    start = (x, y)
    queue = deque([start])
    visited = {start}
    distances = {start: 0}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    while queue:
        current = queue.popleft()
        cx, cy = current

        # Если на клетке есть монетки, запоминаем её
        coin_amount = check("gold", cx, cy)
        if coin_amount:
            coins[current] = coin_amount

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if check("wall", nx, ny):
                continue
            neighbor = (nx, ny)
            # Добавляем ребро в граф
            if current in graph:
                if neighbor not in graph[current]:
                    graph[current].append(neighbor)
            else:
                graph[current] = [neighbor]
            # Если соседняя клетка ещё не посещалась – добавляем её в очередь
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                # Если max_distance задан, то проверяем, не превышен ли он
                if max_distance is None or distances[neighbor] <= max_distance:
                    queue.append(neighbor)
    return graph, coins


def universal_strategy(check, x, y) -> str:
    graph, coins = draw_graph(check, x, y)
    print(f"{graph}\n{coins}\n")

    # Если в области поиска нет монеток – выбираем любое свободное направление.
    if not coins:
        for direction, (dx, dy) in zip(["up", "down", "left", "right"],
                                       [(0, -1), (0, 1), (-1, 0), (1, 0)]):
            if not check("wall", x + dx, y + dy):
                return direction
        return "pass"

    start = (x, y)
    queue = deque([start])
    came_from = {start: None}
    target = None

    # Ищем монетку
    while queue:
        current = queue.popleft()
        if current in coins:
            target = current
            break
        for neighbor in graph.get(current, []):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if target is None:
        return "pass"

    # Восстанавливаем путь от стартовой клетки до цели
    path = []
    cur = target
    while cur != start:
        prev = came_from[cur]
        path.append((prev, cur))
        cur = prev
    path.reverse()

    if not path:
        return "pass"

    from_cell, to_cell = path[0]
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]
    if dx == -1 and dy == 0:
        return "left"
    elif dx == 1 and dy == 0:
        return "right"
    elif dx == 0 and dy == -1:
        return "up"
    elif dx == 0 and dy == 1:
        return "down"
    return "pass"


def level1(check, x, y):
    if check("wall", x + 2, y):
        return "down"
    return "right"


def script(check, x, y):
    if check("gold", x, y):
        return "take"

    return universal_strategy(check, x, y)
