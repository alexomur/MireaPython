from collections import deque
import random

DEBUG = False


def debug_print(*args):
    if DEBUG:
        print(*args)


def draw_graph(check, x, y, max_distance=None) -> (dict, dict):
    """
    Составляет граф доступных клеток, начиная с позиции (x, y), используя обход в ширину (BFS).
    Если max_distance=None, обход идёт по всему достижимому компоненту связности.

    Возвращает два словаря:
      - graph: ключ – координата (x, y), значение – список соседних координат (без стен)
      - coins: ключ – координата (x, y), значение – количество монеток на клетке
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

        coin_amount = check("gold", cx, cy)
        if coin_amount:
            coins[current] = coin_amount

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if check("wall", nx, ny):
                continue
            neighbor = (nx, ny)
            if current in graph:
                if neighbor not in graph[current]:
                    graph[current].append(neighbor)
            else:
                graph[current] = [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                if max_distance is None or distances[neighbor] <= max_distance:
                    queue.append(neighbor)
    return graph, coins


def bfs_path(graph, start, goal):
    """
    Находит кратчайший путь от start до goal по графу.
    Возвращает список координат (путь от start до goal) или None, если путь не найден.
    """
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in graph.get(current, []):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


def best_path(check, graph, coins, start):
    """
    Строит маршрут, по которому бот сможет собрать как можно больше монет.
    Алгоритм действует жадно: из текущей позиции для каждой оставшейся монетки ищется кратчайший путь.

    Нововведение:
      - Учитывается, что взятие монетки занимает 1 тик.
      - Если противник уже стоит на монетке, он заберёт её раньше.
      - В оценке пути теперь учитывается +1 к расстоянию бота.

    Окончательная оценка:
      score = (ценность монетки + бонус) / ((расстояние_бота + 1 + 1) * (1 + опасность)) * штраф_за_противника
    """
    route = [start]
    current = start
    remaining_coins = coins.copy()

    # Собираем позиции противников, видимых в построенном графе
    opponents = []
    for node in graph:
        if check("player", node[0], node[1]):
            opponents.append(node)

    while remaining_coins:
        candidate_paths = []
        for coin_pos, coin_value in remaining_coins.items():
            path = bfs_path(graph, current, coin_pos)
            if not path:
                continue
            distance = len(path) - 1  # число шагов до монетки

            # Считаем опасность пути: число клеток, где есть противники (кроме стартовой)
            danger_count = 0
            for pos in path[1:]:
                if check("player", pos[0], pos[1]):
                    danger_count += 1

            # Бонус за скопление монет: смотрим соседние клетки монетки
            cluster_bonus = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (coin_pos[0] + dx, coin_pos[1] + dy)
                if neighbor in remaining_coins:
                    cluster_bonus += remaining_coins[neighbor]
            total_value = coin_value + cluster_bonus

            # Вычисляем штрафной коэффициент: проверяем, насколько быстро противник может добраться до монетки
            penalty = 1.0
            if opponents:
                opp_distances = []
                for opp in opponents:
                    opp_path = bfs_path(graph, opp, coin_pos)
                    if opp_path is not None:
                        opp_distance = len(opp_path) - 1
                        opp_distances.append(opp_distance)

                if opp_distances:
                    min_opp_distance = min(opp_distances)

                    # **Коррекция учёта времени на подбор монетки**
                    if min_opp_distance == 0:
                        # Противник уже стоит на монетке и поднимет её в следующий тик -> мы не успеваем
                        penalty = 0.1  # Огромный штраф, смысла идти нет
                    elif min_opp_distance < (distance + 1):  # Боту требуется +1 тик на подбор
                        penalty = min_opp_distance / (distance + 1)
                    else:
                        penalty = 1.0

            # Итоговая оценка кандидата
            score = total_value / ((distance + 1 + 1) * (1 + danger_count)) * penalty  # +1 тик на подбор
            candidate_paths.append((score, path, coin_pos))

        if candidate_paths:
            candidate_paths.sort(key=lambda x: x[0], reverse=True)
            best_score, best_segment, best_coin = candidate_paths[0]
            if best_score <= 0.001:
                break
            route.extend(best_segment[1:])
            current = best_coin
            del remaining_coins[best_coin]
        else:
            # Резервный вариант: выбираем ближайшее доступное движение
            fallback_moves = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if not check("wall", nx, ny):
                    danger = 1 if check("player", nx, ny) else 0
                    fallback_moves.append((danger, (nx, ny)))
            if fallback_moves:
                fallback_moves.sort(key=lambda x: x[0])
                chosen_move = fallback_moves[0][1]
                route.append(chosen_move)
            break

    return route


def universal_strategy(check, x, y) -> str:
    graph, coins = draw_graph(check, x, y)
    debug_print(f"Graph: {graph}\nCoins: {coins}\n")

    # Если в области поиска нет монеток – выбираем любое доступное направление.
    if not coins:
        for direction, (dx, dy) in zip(["up", "down", "left", "right"],
                                       [(0, -1), (0, 1), (-1, 0), (1, 0)]):
            if not check("wall", x + dx, y + dy):
                return direction
        return "pass"

    start = (x, y)
    route = best_path(check, graph, coins, start)
    debug_print(f"Planned route: {route}")

    # Если маршрут состоит менее чем из двух шагов, выбираем резервное движение.
    if len(route) < 2:
        for direction, (dx, dy) in zip(["up", "down", "left", "right"],
                                       [(0, -1), (0, 1), (-1, 0), (1, 0)]):
            if not check("wall", x + dx, y + dy):
                return direction
        return "pass"

    next_cell = route[1]
    dx = next_cell[0] - x
    dy = next_cell[1] - y
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
