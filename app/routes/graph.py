"""Graph API route handlers."""

import logging

from fastapi import APIRouter, HTTPException

from app.algorithms.graph import GRAPH_REGISTRY
from app.data.graph_metadata import GRAPH_ALGORITHM_INFO, GRAPH_CODE_SNIPPETS
from app.models.schemas import GraphSolveRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["graph"])


@router.post("/graph-solve")
async def graph_solve(payload: GraphSolveRequest):
    try:
        graph = payload.graph
        algorithm = payload.algorithm
        start = payload.start
        directed = payload.directed
        target = payload.target

        # Ensure weights are numeric
        for node in graph:
            if isinstance(graph[node], dict):
                graph[node] = {k: float(v) for k, v in graph[node].items()}

        if not graph:
            raise HTTPException(status_code=400, detail="Graph cannot be empty")
        if start not in graph:
            raise HTTPException(status_code=400, detail=f"Start node '{start}' not in graph")
        if algorithm not in GRAPH_REGISTRY:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {algorithm}")

        solve_fn = GRAPH_REGISTRY[algorithm]
        steps = solve_fn(graph, start, directed, target=target)

        logger.info("Graph %s from '%s' on %d nodes", algorithm, start, len(graph))
        return {"steps": steps, "algorithm": algorithm}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in graph_solve")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph-algorithm-info/{algorithm}")
async def get_graph_algorithm_info(algorithm: str):
    if algorithm not in GRAPH_ALGORITHM_INFO:
        raise HTTPException(status_code=404, detail=f"Graph algorithm '{algorithm}' not found")
    return GRAPH_ALGORITHM_INFO[algorithm]


@router.get("/graph-algorithm-code/{algorithm}")
async def get_graph_algorithm_code(algorithm: str):
    if algorithm not in GRAPH_CODE_SNIPPETS:
        raise HTTPException(status_code=404, detail=f"Graph algorithm '{algorithm}' not found")
    return {
        "algorithm": algorithm,
        "language": "python",
        "code": GRAPH_CODE_SNIPPETS[algorithm]["python"],
    }
