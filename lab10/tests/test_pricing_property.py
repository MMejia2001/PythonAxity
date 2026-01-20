import pytest
from hypothesis import given
from hypothesis import strategies as st

from lab_tdd.pricing import Item, subtotal

# strategy: lista de items válidos
valid_items = st.lists(
    st.builds(
        Item,
        sku=st.text(min_size=1, max_size=10),
        unit_price=st.floats(
            min_value=0, max_value=10_000, allow_nan=False, allow_infinity=False
        ),
        qty=st.integers(min_value=1, max_value=100),
    ),
    min_size=1,
    max_size=50,
)


@pytest.mark.slow
@given(valid_items)
def test_subtotal_is_never_negative(items):
    assert subtotal(items) >= 0


@pytest.mark.slow
@given(valid_items)
def test_subtotal_equals_sum_of_lines(items):
    expected = round(sum(i.unit_price * i.qty for i in items), 2)
    assert subtotal(items) == expected
