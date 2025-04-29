import math
import deal
import numpy as np
from contextlib import contextmanager

@contextmanager
def raises(expected_exception):
    """
    Просто для проверки возникновения исключений
    """
    try:
        yield
    except expected_exception as e:
        print(f'Ура! Поймали :) {e}')
    except Exception as e:
        print(f"Ожидалось исключение {expected_exception.__name__}, но возникло {type(e).__name__}: {e}")
        raise AssertionError(f"Ожидалось исключение {expected_exception.__name__}, но возникло {type(e).__name__}: {e}")
    else:
        print(f"Ожидалось исключение {expected_exception.__name__}, но оно не возникло.")
        raise AssertionError(f"Ожидалось исключение {expected_exception.__name__}, но оно не возникло.")



@deal.pre(lambda x, y: None not in [x, y])
@deal.pre(lambda x, y: len(x) > 0 and len(y) > 0)
@deal.pre(lambda x, y: isinstance(x, list | tuple) and isinstance(y, list | tuple))
@deal.pre(lambda x, y: len(x) == len(y))
@deal.pre(lambda x, y: all(isinstance(i, (int, float)) for i in x) and all(isinstance(i, (int, float)) for i in y))
#--------------------------------------------------------------------------------------------------------------------
@deal.pure  # 3.7
#--------------------------------------------------------------------------------------------------------------------
@deal.post(lambda result: isinstance(result, (int, float)))  # 3.8
@deal.post(lambda result: result >= 0)  # 3.9
#--------------------------------------------------------------------------------------------------------------------
def euclidean_distance(x: list[float] | tuple[float, ...], y: list[float] | tuple[float, ...]) -> float:
    """
    Функция для вычисления евклидова расстояния между двумя векторами.
    Входные параметры: x и y — кортежи или списки, содержащие числа.
    """
    print("Проводятся дорогостоящие вычисления!")
    v1 = np.array(x)
    v2 = np.array(y)
    return np.linalg.norm(v2 - v1)


# Для тестирования ошибок

with raises(deal.PreContractError):
    euclidean_distance([], [])

with raises(deal.PreContractError):
    euclidean_distance("string", [])

with raises(deal.PreContractError):
    euclidean_distance([1, 2, 3], [1, 2])

with raises(deal.PreContractError):
    euclidean_distance([1, 2, "3"], [1, 2, 3])

with raises(deal.PreContractError): # 3.7
    euclidean_distance([1.0, 2.5], [1.0, "2.5"])

#--------------------------------------------------------------------------------------------------------------------
#  3.7: Проверка на чистоту вывода
with raises(deal.SilentContractError):
    euclidean_distance([0, 0], [1, 1])

#--------------------------------------------------------------------------------------------------------------------
#  3.8: Проверка, что результат функции — число (целое или вещественное)
@deal.post(lambda result: isinstance(result, (int, float)))
def broken_distance_not_number(x, y):
    return "not a number"


 #  3.8: Проверка, что результат — число
with raises(deal.PostContractError):
    broken_distance_not_number([None], [0])


#  3.9: Проверка, что результат функции — неотрицательное число
@deal.post(lambda result: result >= 0)
def broken_distance_negative(x, y):
    return -1


#  3.9: Проверка, что результат функции >= 0
with raises(deal.PostContractError):
    broken_distance_negative([0], [0])
#--------------------------------------------------------------------------------------------------------------------
