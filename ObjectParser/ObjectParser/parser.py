import json
import numbers
import os
from pathlib import Path
from typing import Any, Type, get_origin, get_args

import yaml


def create_instance(cls: Any) -> Any:
    """
    Создает новый экземпляр объекта заданного типа.

    Если переданный тип является generic alias (например, list[int] или dict[str, int]),
    функция использует его базовый тип для создания экземпляра.

    :param cls: Тип, экземпляр которого нужно создать.
    :return: Новый экземпляр объекта.
    :raises TypeError: Если переданный аргумент не является типом или его невозможно инстанцировать.
    """
    origin = get_origin(cls)
    if origin is not None:
        # Если cls — generic alias, то используем базовый тип (origin)
        try:
            return origin()
        except Exception as e:
            raise TypeError(f"Невозможно создать экземпляр для generic alias {cls}") from e

    # Если это обычный класс
    if isinstance(cls, type):
        try:
            # Создаем объект без вызова __init__
            return cls.__new__(cls)
        except Exception as e:
            raise TypeError(f"Невозможно создать экземпляр типа {cls}") from e

    raise TypeError(f"'{cls}' не является корректным типом для создания экземпляра.")


def is_elementary(obj: Any) -> bool:
    """
    Проверяет, является ли объект базовым простым типом:

    - числом (int, float, complex — numbers.Number)
    - строкой (str)
    - None

    :param obj: Объект для проверки.
    :return: True, если объект базового типа, иначе False.
    """
    return isinstance(obj, (numbers.Number, str, type(None)))


def to_simple(obj: Any) -> Any:
    """
    Рекурсивно «упрощает» объект до структур данных Python:

    - Числа, строки и None возвращаются как есть.
    - Списки и кортежи превращаются в списки простых объектов или словарей.
    - Словари превращаются в словари простых объектов или словарей.
    - Пользовательские объекты превращаются в словарь по их публичным атрибутам.

    :param obj: Исходный объект.
    :return: Упрощённая структура (число, строка, список, словарь или None).
    """

    # 1) Базовые простые объекты
    if is_elementary(obj):
        return obj

    # 2) Списки или кортежи
    if isinstance(obj, (list, tuple)):
        return [to_simple(item) for item in obj]

    # 3) Словари
    if isinstance(obj, dict):
        return {k: to_simple(v) for k, v in obj.items()}

    # 4) Обычный объект (экземпляр класса)
    result = {}
    for key in dir(obj):
        if not key.startswith("_"):
            attr_value = getattr(obj, key)
            if not callable(attr_value):
                result[key] = to_simple(attr_value)
    return result


def to_obj(data: Any, cls: Any) -> Any:
    """
    Рекурсивно восстанавливает объект заданного типа из данных,
    используя аннотации полей (типизацию).

    Поддерживаются:
      - Generic-типы (например, list[int], dict[str, SomeClass])
      - Пользовательские классы с __annotations__
      - Примитивные типы – возвращаются как есть

    :param data: Сериализованные данные (например, dict или list).
    :param cls: Целевой тип, который нужно получить.
    :return: Восстановленный объект.
    """
    origin = get_origin(cls)
    if origin is not None:
        args = get_args(cls)
        if origin is list and isinstance(data, list):
            return [
                to_obj(item, args[0]) if isinstance(item, (dict, list)) else item
                for item in data
            ]
        elif origin is dict and isinstance(data, dict):
            key_type, val_type = args
            new_dict = {}
            for k, v in data.items():
                if isinstance(k, (dict, list)):
                    k = to_obj(k, key_type)
                if isinstance(v, (dict, list)):
                    v = to_obj(v, val_type)
                new_dict[k] = v
            return new_dict
        else:
            return to_obj(data, origin)

    # Если у класса нет аннотаций, возвращаем data как есть
    if not hasattr(cls, '__annotations__'):
        return data

    # Создаём объект через create_instance, без вызова __init__
    obj = create_instance(cls)
    annotations = getattr(cls, '__annotations__', {})

    for key, value in data.items():
        if key in annotations:
            attr_type = annotations[key]
            attr_origin = get_origin(attr_type)
            if attr_origin is not None:
                args = get_args(attr_type)
                if attr_origin is list and isinstance(value, list):
                    value = [
                        to_obj(item, args[0]) if isinstance(item, (dict, list)) else item
                        for item in value
                    ]
                elif attr_origin is dict and isinstance(value, dict):
                    key_type, val_type = args
                    new_d = {}
                    for k, v in value.items():
                        if isinstance(k, (dict, list)):
                            k = to_obj(k, key_type)
                        if isinstance(v, (dict, list)):
                            v = to_obj(v, val_type)
                        new_d[k] = v
                    value = new_d
            elif isinstance(value, dict):
                value = to_obj(value, attr_type)
        setattr(obj, key, value)

    return obj


class Parser:
    """
    Статический класс (не предполагает создание экземпляров) для
    сериализации/десериализации объектов в YAML/JSON.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Запрещаем создание экземпляра через обычный конструктор.
        """
        raise Exception(f"Class {Parser.__name__} is a static class!")

    @staticmethod
    def _load_data(path: str or Path, mode: str = "yaml") -> dict:
        """
        Загружает данные из указанного файла.

        :param path: Путь к файлу.
        :param mode: Формат файла ('yaml', 'yml', или 'json').
        :return: Словарь, считанный из файла (или пустой dict, если файл пуст).
        """
        if mode in ("yaml", "yml"):
            with open(path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        elif mode == "json":
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        raise ValueError(f"Неподдерживаемый режим: {mode}")

    @staticmethod
    def _save_data(data: dict or list, path: str or Path, mode: str = "yaml") -> None:
        """
        Сохраняет словарь или список в указанный файл в формате YAML или JSON.
        Если директория для файла не существует, она создаётся.

        :param data: Словарь или список для сохранения.
        :param path: Путь к файлу.
        :param mode: Формат файла ('yaml' или 'json').
        """
        # Определяем директорию из пути и создаем её, если она не существует.
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if mode == "yaml":
            with open(path, "w", encoding="utf-8") as file:
                yaml.dump(
                    data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True
                )
        elif mode == "json":
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False
                )
        else:
            raise ValueError(f"Неподдерживаемый режим: {mode}")

    @staticmethod
    def _get_default_data(cls: Type[object]) -> dict:
        """
        Собирает значения, определённые в классе (Config) как публичные атрибуты.

        :param cls: Класс, из которого берутся значения (по умолчанию Config).
        :return: Словарь {имя атрибута: значение}.
        """
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith("_") and not callable(getattr(cls, key))
        }

    @staticmethod
    def load(path: str or Path, cls: Any, mode: str = "yaml") -> Any:
        """
        Загружает файл конфигурации или данных и создаёт объект указанного класса.
        Если файл не существует, создаёт его с дефолтными значениями.

        :param path: Путь к файлу конфигурации.
        :param cls: Класс, экземпляр которого нужно создать.
        :param mode: Формат файла ('yaml' или 'json').
        :return: Экземпляр класса cls, заполненный данными из файла.
        """
        # Получаем дефолтные данные для указанного класса
        default_data: dict = Parser._get_default_data(cls)
        modified = False

        data_dict: dict or list
        data_inst: cls

        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            data_dict = default_data.copy()
            Parser._save_data(data_dict, path, mode)
        else:
            loaded_raw = Parser._load_data(path, mode)
            # Рекурсивно преобразуем загруженные данные в объект нужного типа
            data_instance = to_obj(loaded_raw, cls)

            # Если объект поддерживает __dict__, добавляем недостающие поля
            if hasattr(data_instance, '__dict__'):
                for key, value in default_data.items():
                    if key not in data_instance.__dict__:
                        data_instance.__dict__[key] = value
                        modified = True
                if modified:
                    Parser._save_data(data_instance.__dict__, path, mode)
                data_dict = data_instance.__dict__
            else:
                # Если data_dict не поддерживает __dict__ (например, список или словарь),
                # можем выполнить проверку на наличие ключей, если это словарь, или оставить как есть.
                if isinstance(data_instance, dict):
                    for key, value in default_data.items():
                        if key not in data_instance:
                            data_instance[key] = value
                            modified = True
                    if modified:
                        Parser.save(data_instance, path, mode)
                data_dict = data_instance

        # Создаем инстанс объекта заданного типа
        data_inst = create_instance(cls)
        # Если инстанс поддерживает обновление через __dict__, производим слияние
        if hasattr(data_inst, '__dict__'):
            data_inst.__dict__.update(data_dict)
        else:
            # Если объект не имеет __dict__ (например, list или dict),
            # возвращаем непосредственно data_dict
            data_inst = data_dict

        return data_inst

    @staticmethod
    def save(data: Any, path: str or Path, mode: str = "yaml") -> None:
        """
        Сериализует объект (рекурсивно) и сохраняет его в файл.

        :param data: Объект для сохранения (например, экземпляр класса).
        :param path: Путь к файлу сохранения.
        :param mode: Формат файла ('yaml' или 'json').
        """
        simplified_data = to_simple(data)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        Parser._save_data(simplified_data, path, mode)

__all__ = ["Parser", "create_instance", "is_elementary", "to_simple", "to_obj"]