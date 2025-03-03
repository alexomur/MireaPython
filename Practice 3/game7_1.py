import random
import os


class Action:
    def __init__(self, text: str, result: str, target: str = None, action_type: str = "move", correct: bool = None,
                 escape_fail_target: str = None):
        """
        text: Текст действия, отображаемый игроку.
        result: Сообщение, которое выводится после выбора действия.
        target: Метка целевой комнаты при успешном исходе.
        action_type: Тип действия – "move", "escape" или "fight".
        correct: Для сражения – True, если выбранный вариант является верным.
        escape_fail_target: Для побега – метка комнаты при неудаче.
        """
        self.text = text
        self.result = result
        self.target = target
        self.action_type = action_type
        self.correct = correct
        self.escape_fail_target = escape_fail_target


class Room:
    def __init__(self, name: str, label: str, actions: list, dangerous: bool = False):
        """
        name: Название комнаты.
        label: Уникальная метка комнаты.
        actions: Список объектов Action.
        dangerous: Флаг, указывающий, что комната опасна.
        """
        self.name = name
        self.label = label
        self.actions = actions
        self.dangerous = dangerous

    def description(self) -> str:
        phrases = [
            "Здесь прохладно и тихо.",
            "Вы слышите эхо своих шагов.",
            "Комната освещена тусклым светом.",
            "Тусклый свет проникает сквозь пыльные окна.",
            "Стены украшены древними узорами.",
            "Здесь чувствуется легкое волнение.",
            "Обстановка напоминает заброшенное место."
        ]
        desc = f"{self.name}\n\n{random.choice(phrases)}\n"
        if self.dangerous:
            desc += "\nВнимание! В этой комнате МОНСТР1!!1! Нужно быстро принять решение!\n"
        return desc

    def show_actions(self) -> str:
        if not self.actions:
            return "Нет доступных действий."
        return "\n".join(f"{idx}. {action.text}" for idx, action in enumerate(self.actions, start=1))


def build_game_graph() -> dict:
    """
    Строит граф из 10+ комнат, где каждая комната (за исключением терминальных)
    имеет переходы в другие, что обеспечивает возможность добраться от любой комнаты до любой.

    Опасные комнаты (room3 и room7) содержат варианты побега и сражения.
    """
    graph = {}

    # Стартовая комната
    graph["start"] = Room("Начало лабиринта", "start", actions=[
        Action("Идите на север", "Вы идете на север.", target="room1"),
        Action("Идите на восток", "Вы идете на восток.", target="room2"),
        Action("Осмотреться", "Вы оглядываетесь вокруг, но лабиринт пока молчит.")
    ])

    # Комната 1
    graph["room1"] = Room("Комната 1", "room1", actions=[
        Action("Идите на север", "Вы направляетесь на север.", target="room4"),
        Action("Идите на восток", "Вы идете на восток.", target="room3"),
        Action("Идите на юг", "Вы возвращаетесь назад.", target="start")
    ])

    # Комната 2
    graph["room2"] = Room("Комната 2", "room2", actions=[
        Action("Идите на запад", "Вы возвращаетесь к началу.", target="start"),
        Action("Идите на север", "Вы идете на север.", target="room3"),
        Action("Идите на восток", "Вы идете на восток.", target="room5")
    ])

    # Опасная комната 3
    graph["room3"] = Room("Комната 3 (опасная)", "room3", dangerous=True, actions=[
        Action("Попытаться сбежать", "Вы пытаетесь сбежать...", target="room4", action_type="escape",
               escape_fail_target="dead"),
        Action("Сражаться мечом", "Вы пытаетесь сразиться мечом.", target="room4", action_type="fight", correct=True),
        Action("Сражаться кулаками", "Вы отчаянно деретесь, но без успеха!", target="dead", action_type="fight",
               correct=False),
        Action("Осмотреться", "Вы осматриваетесь, пытаясь найти слабое место.")
    ])

    # Комната 4
    graph["room4"] = Room("Комната 4", "room4", actions=[
        Action("Идите на восток", "Вы идете на восток.", target="room5"),
        Action("Идите на юг", "Вы возвращаетесь в Комнату 1.", target="room1"),
        Action("Идите на север", "Вы идете на север.", target="room6")
    ])

    # Комната 5
    graph["room5"] = Room("Комната 5", "room5", actions=[
        Action("Идите на запад", "Вы идете на запад.", target="room2"),
        Action("Идите на север", "Вы идете на север.", target="room6"),
        Action("Идите на восток", "Вы идете на восток.", target="room7")
    ])

    # Комната 6
    graph["room6"] = Room("Комната 6", "room6", actions=[
        Action("Идите на юг", "Вы возвращаетесь в Комнату 4.", target="room4"),
        Action("Идите на восток", "Вы идете на восток.", target="room7"),
        Action("Идите на север", "Вы идете на север.", target="room8")
    ])

    # Опасная комната 7
    graph["room7"] = Room("Комната 7 (опасная)", "room7", dangerous=True, actions=[
        Action("Попытаться сбежать", "Вы пытаетесь сбежать...", target="room6", action_type="escape",
               escape_fail_target="dead"),
        Action("Сражаться магией", "Вы применяете магию, но это не помогает!", target="dead", action_type="fight",
               correct=False),
        Action("Сражаться луком", "Ваш выстрел из лука точен!", target="room8", action_type="fight", correct=True),
        Action("Осмотреться", "Вы быстро осматриваетесь в поисках подсказок.")
    ])

    # Комната 8
    graph["room8"] = Room("Комната 8", "room8", actions=[
        Action("Идите на запад", "Вы возвращаетесь в Комнату 6.", target="room6"),
        Action("Идите на север", "Вы идете на север, впереди свет.", target="end"),
        Action("Идите на юг", "Вы возвращаетесь в Комнату 7.", target="room7"),
        Action("Осмотреться", "Вы замечаете, что здесь всё кажется знакомым.")
    ])

    # Конечная комната (выход)
    graph["end"] = Room("Выход", "end", actions=[
        Action("Осмотреться", "Вы видите свободу за пределами лабиринта. Игра окончена.")
    ])

    # Комната поражения (игрок погиб)
    graph["dead"] = Room("Поражение", "dead", actions=[], dangerous=False)

    return graph


def play_game(graph: dict):
    """
    Основной игровой цикл.
    Для каждого действия:
      - Если тип "move" – осуществляется переход в указанную комнату.
      - Если тип "escape" – с вероятностью 50% переход по target, иначе по escape_fail_target.
      - Если тип "fight" – проверяется, верен ли выбор: верное сражение переводит в target, неверное – в target (обычно это комната поражения).
    Игра завершается при попадании в комнаты с метками "end" или "dead", либо если нет доступных действий.
    """
    current_room = graph["start"]
    result = ""
    while True:
        os.system('cls')

        print(result + current_room.description())
        result = ""

        if not current_room.actions:
            print("Нет доступных действий. Игра окончена.")
            break

        print("Доступные действия:")
        print(current_room.show_actions())
        user_input = input("> ")
        try:
            choice = int(user_input.strip())
            if 1 <= choice <= len(current_room.actions):
                chosen_action = current_room.actions[choice - 1]
                result += (f"\n{chosen_action.result}\n")

                # Обработка действия в зависимости от типа
                if chosen_action.action_type == "escape":
                    if random.random() < 0.5:
                        result += ("Побег удался!\n")
                        next_label = chosen_action.target
                    else:
                        result += ("Побег не удался!\n")
                        next_label = chosen_action.escape_fail_target
                elif chosen_action.action_type == "fight":
                    if chosen_action.correct:
                        result += ("Сражение прошло успешно!\n")
                        next_label = chosen_action.target
                    else:
                        result += ("Сражение закончилось неудачей!\n")
                        next_label = chosen_action.target
                else:
                    next_label = chosen_action.target

                # Если действие не предполагает переход (target == None), остаёмся в текущей комнате
                if next_label:
                    if next_label not in graph:
                        print("Неизвестная комната. Игра завершена.")
                        break
                    current_room = graph[next_label]
                # Если переход не задан, остаёмся в той же комнате
            else:
                result += ("Неверный выбор. Попробуйте ещё раз.\n")
        except ValueError:
            print("Пожалуйста, введите число, соответствующее вашему выбору.\n")

        if current_room.label in ["end", "dead"]:
            print(current_room.description())
            if current_room.label == "dead":
                print("Вы потерпели поражение. Игра окончена.")
            else:
                print("Игра окончена.")
            break


if __name__ == "__main__":
    game_graph = build_game_graph()
    play_game(game_graph)
