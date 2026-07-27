# ====================================================
# TEST FILE used for validating the class definitions
# RUN THE TESTS WITH: pytest tests.py -v
# ====================================================
from typing import Optional

import pytest  # type: ignore

from building_types import (
    Blueprint,
    Building,
    Commercial,
    Industry,
    Park,
    Residential,
    Road,
)
from grid import Grid


@pytest.fixture
def grid() -> Grid:
    return Grid(size=20)


def test_set(grid: Grid) -> None:
    grid.set(1, 1, Park())
    assert isinstance(grid.data[1][1], Park)

    grid.set(3, 2, Blueprint(Road()))
    assert isinstance(grid.data[3][2], Blueprint)

    grid.set(7, 9, Residential())
    grid.set(7, 9, None)
    assert grid.data[7][9] is None


def test_get(grid: Grid) -> None:
    grid.set(1, 1, Residential())
    b = grid.get(1, 1)
    assert isinstance(b, Residential)

    grid.set(4, 6, Industry())
    b = grid.get(4, 6)
    assert isinstance(b, Industry)

    b = grid.get(9, 9)
    assert b is None

    with pytest.raises(IndexError):
        grid.get(21, 21)


def test_safe_get(grid: Grid) -> None:
    test_get(grid)
    b = grid.safe_get(21, 21)
    assert b is None


def test_resolve_get(grid: Grid) -> None:
    test_safe_get(grid)
    grid.set(3, 3, Blueprint(Commercial()))
    b = grid.resolve_get(3, 3)
    assert isinstance(b, Commercial)


def test_is_empty(grid: Grid) -> None:
    res = grid.is_empty()
    assert res is True

    grid.set(1, 1, Residential())
    res = grid.is_empty()
    assert res is False

    grid.set(1, 1, None)
    res = grid.is_empty()
    assert res is True


def test_has_real_buildings(grid: Grid) -> None:
    grid.set(1, 1, Residential())
    res = grid.has_real_buildings()
    assert res is True

    grid.set(1, 1, None)
    res = grid.has_real_buildings()
    assert res is False

    grid.set(1, 1, Blueprint(Commercial()))
    res = grid.has_real_buildings()
    assert res is False

    grid.set(2, 2, Industry())
    res = grid.has_real_buildings()
    assert res is True


def test_is_real_building(grid: Grid) -> None:
    grid.set(1, 1, Residential())
    res = grid.is_real_building(Residential())
    assert res is True

    res = grid.is_real_building(None)
    assert res is False

    res = grid.is_real_building(Blueprint(Road()))
    assert res is False


def test_has_building_on_border(grid: Grid) -> None:
    grid.set(1, 1, Residential())
    res = grid.has_building_on_border()
    assert res is False

    grid.set(0, 0, Commercial())
    res = grid.has_building_on_border()
    assert res is True

    grid.set(0, 0, Blueprint(Commercial()))
    res = grid.has_building_on_border()
    assert res is False

    grid.set(0, 2, Industry())
    res = grid.has_building_on_border()
    assert res is True

    grid.set(0, 2, None)
    grid.set(19, 11, Park())
    res = grid.has_building_on_border()
    assert res is True

    grid.set(19, 11, None)
    grid.set(7, 19, Road())
    res = grid.has_building_on_border()
    assert res is True


@pytest.mark.parametrize("increase", [1, 2, 5, 10, 25])
def test_expand_grid(increase: int) -> None:
    base_size = 5
    grid = Grid(size=base_size)
    grid.expand_grid(increase)
    assert grid.size == base_size + (increase * 2)


@pytest.mark.parametrize(
    ("buildings", "expected"),
    [
        ([(1, 1, Residential())], (0, 0)),  # R: 0, 0 (+1 inc / -1 upkeep)
        (
            [(1, 1, Residential()), (1, 2, Road())],
            (1, -1),
        ),  # R: (0, 0) *: +1 score, -1 upkeep
        (
            [(1, 1, Residential()), (1, 2, Road()), (1, 3, Park())],
            (3, -1),
        ),  # R: (+2, 0) *: (+1, 0), O: (0, -1)
        (
            [
                (1, 1, Residential()),
                (1, 2, Road()),
                (2, 1, Residential()),
                (2, 2, Road()),
            ],
            (4, 1),  # R: (+1 * 2, +2 / -1), *: (+2, 0)
        ),
        (
            [(1, 1, Residential()), (1, 2, Road()), (1, 3, Industry())],
            (2, 1),
        ),  # R: (0, 0), *: (+1, 0), I: (+1, +1)
        ([(1, 1, Residential()), (1, 2, Road()), (2, 1, Industry())], (3, 0)),
    ],
)
def test_calculate_turn(
    buildings: list[tuple[int, int, Optional[Blueprint | Building]]],
    expected: tuple[int, int],
) -> None:
    grid: Grid = Grid(size=5)
    for x, y, building in buildings:
        grid.set(x, y, building)

    score, income = grid.calculate_turn()
    assert (score, income) == expected
