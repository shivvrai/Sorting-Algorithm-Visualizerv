"""Unit tests for sorting algorithms."""

import pytest
from app.algorithms.sorting import SortingAlgorithms, SORTING_REGISTRY


# ---- Parametrize across all algorithms ----
ALGORITHMS = list(SORTING_REGISTRY.keys())


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_sorts_correctly(algo):
    arr = [5, 3, 8, 1, 2]
    steps = SORTING_REGISTRY[algo](arr)
    final = steps[-1]
    assert final["type"] == "done"
    assert final["array"] == sorted(arr)


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_already_sorted(algo):
    arr = [1, 2, 3, 4, 5]
    steps = SORTING_REGISTRY[algo](arr)
    assert steps[-1]["array"] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_reverse_sorted(algo):
    arr = [5, 4, 3, 2, 1]
    steps = SORTING_REGISTRY[algo](arr)
    assert steps[-1]["array"] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_single_element(algo):
    arr = [42]
    steps = SORTING_REGISTRY[algo](arr)
    assert steps[-1]["array"] == [42]


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_duplicates(algo):
    arr = [3, 1, 3, 2, 1]
    steps = SORTING_REGISTRY[algo](arr)
    assert steps[-1]["array"] == sorted(arr)


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_original_not_mutated(algo):
    arr = [5, 3, 8, 1, 2]
    original = arr.copy()
    SORTING_REGISTRY[algo](arr)
    assert arr == original, f"{algo} mutated the input array"


def test_registry_has_all_algorithms():
    expected = {"bubble", "selection", "insertion", "merge", "quick", "heap", "counting"}
    assert set(SORTING_REGISTRY.keys()) == expected


def test_steps_have_required_keys():
    steps = SortingAlgorithms.bubble_sort([3, 1, 2])
    for step in steps:
        assert "type" in step
        assert "array" in step or step["type"] in ("done",)
