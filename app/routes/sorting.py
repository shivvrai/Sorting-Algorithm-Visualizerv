"""Sorting API route handlers."""

import time
import io
import csv
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.algorithms.sorting import SORTING_REGISTRY
from app.data.sorting_metadata import ALGORITHM_INFO
from app.data.sorting_code import CODE_SNIPPETS
from app.models.schemas import SortRequest, TimeTrialRequest, ExportRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["sorting"])

# Space complexity for time trial display
SPACE_COMPLEXITY = {
    "bubble": "O(1)", "selection": "O(1)", "insertion": "O(1)",
    "merge": "O(n)", "quick": "O(log n)", "heap": "O(1)", "counting": "O(k)",
}


@router.post("/sort")
async def sort_array(payload: SortRequest):
    try:
        algorithm = payload.algorithm
        if algorithm not in SORTING_REGISTRY:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {algorithm}")

        array = [int(x) for x in payload.array]
        start_time = time.perf_counter()

        sort_fn = SORTING_REGISTRY[algorithm]
        steps = sort_fn(array)

        end_time = time.perf_counter()
        execution_time_us = (end_time - start_time) * 1_000_000

        final_step = steps[-1]
        logger.info("Sorted %d elements with %s in %.0fμs", len(array), algorithm, execution_time_us)
        return {
            "steps": steps,
            "execution_time_us": round(execution_time_us, 2),
            "algorithm": algorithm,
            "array_size": len(array),
            "total_comparisons": final_step.get("total_comparisons", 0),
            "total_swaps": final_step.get("total_swaps", 0),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in sort_array")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/algorithm-info/{algorithm}")
async def get_algorithm_info(algorithm: str):
    if algorithm not in ALGORITHM_INFO:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' not found")
    return ALGORITHM_INFO[algorithm]


@router.get("/algorithm-code/{algorithm}")
async def get_algorithm_code(algorithm: str, language: str = "python"):
    if algorithm not in CODE_SNIPPETS:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' not found")
    if language not in CODE_SNIPPETS[algorithm]:
        raise HTTPException(status_code=404, detail=f"Language '{language}' not available")
    return {
        "algorithm": algorithm,
        "language": language,
        "code": CODE_SNIPPETS[algorithm][language],
    }


@router.post("/time-trial")
async def time_trial(payload: TimeTrialRequest):
    try:
        array = [int(x) for x in payload.array]
        results = []

        for algo_name, sort_fn in SORTING_REGISTRY.items():
            try:
                start_time = time.perf_counter()
                steps = sort_fn(array)
                end_time = time.perf_counter()
                execution_time_us = (end_time - start_time) * 1_000_000
                final_step = steps[-1]

                results.append({
                    "algorithm": algo_name,
                    "execution_time_us": round(execution_time_us, 2),
                    "comparisons": final_step.get("total_comparisons", 0),
                    "swaps": final_step.get("total_swaps", 0),
                    "total_steps": len(steps),
                    "space_complexity": SPACE_COMPLEXITY.get(algo_name, "?"),
                })
            except Exception as e:
                results.append({"algorithm": algo_name, "error": str(e)})

        results.sort(key=lambda x: x.get("execution_time_us", float("inf")))
        logger.info("Time trial completed for %d elements", len(array))
        return {
            "results": results,
            "array_size": len(array),
            "fastest": results[0]["algorithm"] if results else None,
        }

    except Exception as e:
        logger.exception("Error in time_trial")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_results(data: ExportRequest):
    if data.format == "json":
        return JSONResponse(content=data.results)

    elif data.format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["algorithm", "array_size", "comparisons", "swaps"])
        writer.writeheader()
        writer.writerow(data.results)
        csv_content = output.getvalue()
        return JSONResponse(content={
            "csv": csv_content,
            "filename": f"sorting-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv",
        })

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {data.format}")
