"""Unit tests for graph algorithms."""

import pytest
from app.algorithms.graph import GraphAlgorithms, GRAPH_REGISTRY


SAMPLE_GRAPH = {
    "A": {"B": 4, "D": 2},
    "B": {"A": 4, "C": 5, "D": 1},
    "C": {"B": 5, "F": 3},
    "D": {"A": 2, "B": 1, "E": 7},
    "E": {"D": 7, "F": 1},
    "F": {"C": 3, "E": 1},
}


def test_bfs_visits_all():
    steps = GraphAlgorithms.bfs(SAMPLE_GRAPH, "A", False)
    done = steps[-1]
    assert done["type"] == "done"
    assert set(done["visited"]) == set(SAMPLE_GRAPH.keys())


def test_dfs_visits_all():
    steps = GraphAlgorithms.dfs(SAMPLE_GRAPH, "A", False)
    done = steps[-1]
    assert done["type"] == "done"
    assert set(done["visited"]) == set(SAMPLE_GRAPH.keys())


def test_dijkstra_no_target():
    steps = GraphAlgorithms.dijkstra(SAMPLE_GRAPH, "A", False)
    done = steps[-1]
    assert done["type"] == "done"
    assert done["distances"]["A"] == 0
    # D should be 2 (direct)
    assert done["distances"]["D"] == 2


def test_dijkstra_with_target():
    steps = GraphAlgorithms.dijkstra(SAMPLE_GRAPH, "A", False, target="F")
    done = steps[-1]
    assert done["type"] == "done"
    assert "path" in done
    assert done["path"][0] == "A"
    assert done["path"][-1] == "F"
    assert done["final_distance"] == 10


def test_dijkstra_unreachable():
    graph = {"A": {"B": 1}, "B": {"A": 1}, "C": {}}
    steps = GraphAlgorithms.dijkstra(graph, "A", False, target="C")
    done = steps[-1]
    assert "unreachable" in done["description"].lower() or "❌" in done["description"]


def test_dijkstra_no_inf_in_distances():
    """Ensure float('inf') is never in the distance dicts (JSON can't serialize it)."""
    steps = GraphAlgorithms.dijkstra(SAMPLE_GRAPH, "A", False)
    for step in steps:
        if "distances" in step:
            for v in step["distances"].values():
                assert v != float("inf"), f"float('inf') found in step {step['type']}"


def test_prim_mst():
    steps = GraphAlgorithms.prim(SAMPLE_GRAPH, "A", False)
    done = steps[-1]
    assert done["type"] == "done"
    assert "total_weight" in done
    assert done["total_weight"] > 0


def test_kruskal_mst():
    steps = GraphAlgorithms.kruskal(SAMPLE_GRAPH, "A", False)
    done = steps[-1]
    assert done["type"] == "done"
    assert "total_weight" in done
    assert done["total_weight"] > 0


def test_prim_kruskal_same_weight():
    prim_done = GraphAlgorithms.prim(SAMPLE_GRAPH, "A", False)[-1]
    kruskal_done = GraphAlgorithms.kruskal(SAMPLE_GRAPH, "A", False)[-1]
    assert prim_done["total_weight"] == kruskal_done["total_weight"]


def test_graph_registry_complete():
    expected = {"bfs", "dfs", "dijkstra", "prim", "kruskal"}
    assert set(GRAPH_REGISTRY.keys()) == expected
