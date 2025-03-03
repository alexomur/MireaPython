# visualize_game.py
import game7_1 as game
from graphviz import Digraph

def build_dot_code(game_graph: dict) -> Digraph:
    """
    Принимает граф комнат (словарь, где ключи — метки комнат, а значения — объекты Room)
    и возвращает объект Digraph, содержащий узлы и рёбра игрового мира.
    """
    dot = Digraph(comment="Game Graph")
    dot.attr(rankdir="LR")  # задаём направление графа слева направо

    # Создаём узлы: для стартовой, конечной и поражения задаём особые формы.
    for label, room in game_graph.items():
        if label == "start":
            shape = "Mdiamond"
        elif label == "end":
            shape = "Msquare"
        elif label == "dead":
            shape = "diamond"
        else:
            shape = "ellipse"
        dot.node(label, room.name, shape=shape)

    # Создаём рёбра: для каждого действия, которое ведёт в другую комнату.
    for label, room in game_graph.items():
        for action in room.actions:
            if action.target:
                # В качестве метки ребра используем текст действия
                dot.edge(label, action.target, label=action.text)
    return dot

if __name__ == '__main__':
    # Импортируем граф игрового мира из модуля game
    game_graph = game.build_game_graph()

    # Генерируем dot граф
    dot = build_dot_code(game_graph)

    # Выводим исходный код Dot в консоль
    print(dot.source)

    # Визуализация: сохраняем и открываем граф (файл game_graph.pdf)
    # dot.view() сохраняет файл и открывает его во внешнем просмотрщике
    dot.view(filename="game_graph.dot", cleanup=True)
