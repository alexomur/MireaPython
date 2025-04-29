import deal
import math
from typing import List

distance_function = deal.chain(
    deal.pre(lambda a, b: a is not None and b is not None
              and isinstance(a, (list, tuple)) and isinstance(b, (list, tuple))
              and 0 < len(a) == len(b)
              and all(isinstance(x, (int, float)) for x in a)
              and all(isinstance(y, (int, float)) for y in b)),
    deal.post(lambda r: isinstance(r, (int, float))),
    deal.post(lambda r: r >= 0),
    deal.pure
)

@distance_function
def euclidean_distance(a: List[float], b: List[float]) -> float:
    return math.sqrt(sum((yi - xi) ** 2 for xi, yi in zip(a, b)))

@distance_function
def manhattan_distance(a: List[float], b: List[float]) -> float:
    return sum(abs(yi - xi) for xi, yi in zip(a, b))
