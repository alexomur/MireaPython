import game7_1 as game


def check_dead_ends(game_graph: dict) -> list:
    """
    Возвращает список меток комнат, из которых невозможно добраться до конечной комнаты.
    Терминальные комнаты – с метками "end" или "dead".
    """
    # Строим обратный граф: для каждой комнаты собираем список комнат,
    # из которых можно попасть в неё по действию.
    rev_graph = {room_label: [] for room_label in game_graph}
    for room_label, room in game_graph.items():
        for action in room.actions:
            if action.target is not None:
                rev_graph[action.target].append(room_label)

    terminal_labels = {"end", "dead"}

    reachable = set(terminal_labels)
    stack = list(terminal_labels)

    while stack:
        current = stack.pop()
        for predecessor in rev_graph.get(current, []):
            if predecessor not in reachable:
                reachable.add(predecessor)
                stack.append(predecessor)

    # Тупиковыми считаем комнаты, из которых не достигнуть конечных.
    dead_ends = [label for label in game_graph if label not in reachable]
    return dead_ends


if __name__ == '__main__':
    # Импортируем граф игрового мира из модуля game
    game_graph = game.build_game_graph()

    # Проверяем граф на тупики
    dead_end_rooms = check_dead_ends(game_graph)

    if dead_end_rooms:
        print("Найдены тупиковые комнаты (из которых нельзя добраться до завершения игры):")
        for label in dead_end_rooms:
            room = game_graph[label]
            print(f"{label}: {room.name}")
    else:
        print("Тупиков не найдено. Из любой комнаты можно добраться до завершения игры.")
