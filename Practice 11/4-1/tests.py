from funcs import euclidean_distance, manhattan_distance

from hypothesis import given, strategies as st
import pytest

@st.composite
def list_pairs(draw):
    length = draw(st.integers(min_value=1, max_value=10))
    floats = st.floats(
        min_value=-1e6, max_value=1e6,
        allow_nan=False, allow_infinity=False
    )
    a = draw(st.lists(floats, min_size=length, max_size=length))
    b = draw(st.lists(floats, min_size=length, max_size=length))
    return a, b

@given(list_pairs())
def test_commutativity_euclidean(pair):
    print(pair)
    a, b = pair
    assert euclidean_distance(a, b) == pytest.approx(euclidean_distance(b, a))

@given(list_pairs())
def test_commutativity_manhattan(pair):
    a, b = pair
    assert manhattan_distance(a, b) == manhattan_distance(b, a)