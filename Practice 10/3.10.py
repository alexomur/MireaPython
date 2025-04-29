import math
import deal

# ---------- единая цепочка контрактов -------------------------------------

distance_function = deal.chain(
    deal.pure,

    deal.pre(lambda x, y: None not in (x, y)),
    deal.pre(lambda x, y: isinstance(x, (list, tuple)) and isinstance(y, (list, tuple))),
    deal.pre(lambda x, y: len(x) > 0 and len(y) > 0),
    deal.pre(lambda x, y: len(x) == len(y)),
    deal.pre(
        lambda x, y: all(isinstance(i, (int, float)) for i in x)
        and all(isinstance(i, (int, float)) for i in y)
    ),

    deal.post(lambda result: isinstance(result, (int, float))),
    deal.post(lambda result: result >= 0),
)

# ---------- реализации -----------------------------------------------------


@distance_function
def euclidean_distance(
    x: list[float] | tuple[float, ...],
    y: list[float] | tuple[float, ...],
) -> float:
    """
    Евклидово расстояние

    Примеры
    -------
    >>> euclidean_distance((0, 0), (3, 4))
    5.0
    >>> euclidean_distance([1, 2, 3], [1, 2, 3])
    0.0
    """
    return math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(x, y)))


@distance_function
def manhattan_distance(
    x: list[float] | tuple[float, ...],
    y: list[float] | tuple[float, ...],
) -> float:
    """
    Расстояние Манхэттена

    Примеры
    -------
    >>> manhattan_distance((0, 0), (3, 4))
    7
    >>> manhattan_distance([1, 2, 3], [1, 2, 3])
    0
    """
    return sum(abs(xi - yi) for xi, yi in zip(x, y))


# ---------- запуск doctest -------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
