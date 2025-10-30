"""
SORTING ALGORITHM VISUALIZER - BACKEND
Save as: app.py

Enhanced with:
- Comprehensive education resources
- YouTube & GeeksforGeeks links
- Real-world use cases
- Code walkthroughs
- When to use guidance
- Full algorithm metadata
"""

from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import time
import io
import csv
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Ultimate Sorting Visualizer API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding='utf-8'), status_code=200)
    else:
        return HTMLResponse(content="<h1>Please create index.html in the same directory</h1>")

@app.get("/styles.css")
async def serve_css():
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        return FileResponse(css_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="styles.css not found")

@app.get("/script.js")
async def serve_js():
    js_path = Path(__file__).parent / "script.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="script.js not found")

# ============================================================
# SORTING ALGORITHMS
# ============================================================

class SortingAlgorithms:
    
    @staticmethod
    def bubble_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                steps.append({
                    "type": "compare",
                    "indices": [j, j + 1],
                    "array": arr.copy(),
                    "description": f"Comparing {arr[j]} and {arr[j+1]} at positions {j} and {j+1}",
                    "pass_number": i + 1
                })
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    steps.append({
                        "type": "swapping",
                        "indices": [j, j + 1],
                        "array": arr.copy(),
                        "description": f"Swapped {arr[j+1]} and {arr[j]}",
                        "pass_number": i + 1
                    })
            
            steps.append({
                "type": "sorted",
                "indices": [n - i - 1],
                "array": arr.copy(),
                "description": f"Element {arr[n-i-1]} is now in final position {n-i-1}",
                "pass_number": i + 1
            })
            
            if not swapped:
                break
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Bubble sort completed!",
            "total_comparisons": len([s for s in steps if s["type"] == "compare"]),
            "total_swaps": len([s for s in steps if s["type"] == "swapping"])
        })
        
        return steps

    @staticmethod
    def selection_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            min_idx = i
            
            steps.append({
                "type": "compare",
                "indices": [i],
                "array": arr.copy(),
                "description": f"Finding minimum from position {i} onwards",
                "pass_number": i + 1
            })
            
            for j in range(i + 1, n):
                steps.append({
                    "type": "compare",
                    "indices": [min_idx, j],
                    "array": arr.copy(),
                    "description": f"Current min {arr[min_idx]} vs {arr[j]}",
                    "pass_number": i + 1
                })
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                steps.append({
                    "type": "swapping",
                    "indices": [i, min_idx],
                    "array": arr.copy(),
                    "description": f"Swapped minimum {arr[i]} to position {i}",
                    "pass_number": i + 1
                })
            
            steps.append({
                "type": "sorted",
                "indices": [i],
                "array": arr.copy(),
                "description": f"Position {i} now has {arr[i]} in final place",
                "pass_number": i + 1
            })
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Selection sort completed!",
            "total_comparisons": len([s for s in steps if s["type"] == "compare"]),
            "total_swaps": len([s for s in steps if s["type"] == "swapping"])
        })
        
        return steps

    @staticmethod
    def insertion_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        n = len(arr)
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            steps.append({
                "type": "compare",
                "indices": [i],
                "array": arr.copy(),
                "description": f"Inserting {key} into sorted portion",
                "pass_number": i
            })
            
            while j >= 0 and arr[j] > key:
                steps.append({
                    "type": "compare",
                    "indices": [j, j + 1],
                    "array": arr.copy(),
                    "description": f"{arr[j]} > {key}, shifting right",
                    "pass_number": i
                })
                
                arr[j + 1] = arr[j]
                j -= 1
            
            arr[j + 1] = key
            steps.append({
                "type": "sorted",
                "indices": [j + 1],
                "array": arr.copy(),
                "description": f"Inserted {key} at position {j+1}",
                "pass_number": i
            })
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Insertion sort completed!",
            "total_comparisons": len([s for s in steps if s["type"] == "compare"]),
            "total_swaps": 0
        })
        
        return steps

    @staticmethod
    def merge_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        
        def merge(arr, left, mid, right, depth):
            left_arr = arr[left:mid + 1]
            right_arr = arr[mid + 1:right + 1]
            
            steps.append({
                "type": "compare",
                "indices": list(range(left, right + 1)),
                "array": arr.copy(),
                "description": f"Merging subarrays [{left}..{mid}] and [{mid+1}..{right}]",
                "depth": depth
            })
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                if left_arr[i] <= right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                
                steps.append({
                    "type": "sorted",
                    "indices": [k],
                    "array": arr.copy(),
                    "description": f"Placed {arr[k]} at position {k}",
                    "depth": depth
                })
                k += 1
            
            while i < len(left_arr):
                arr[k] = left_arr[i]
                i += 1
                k += 1
            
            while j < len(right_arr):
                arr[k] = right_arr[j]
                j += 1
                k += 1
        
        def merge_sort_helper(arr, left, right, depth=0):
            if left < right:
                mid = (left + right) // 2
                merge_sort_helper(arr, left, mid, depth + 1)
                merge_sort_helper(arr, mid + 1, right, depth + 1)
                merge(arr, left, mid, right, depth)
        
        merge_sort_helper(arr, 0, len(arr) - 1)
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Merge sort completed!",
            "total_comparisons": len([s for s in steps if s["type"] == "compare"]),
            "total_swaps": 0
        })
        
        return steps

    @staticmethod
    def quick_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        
        def partition(arr, low, high, depth):
            pivot = arr[high]
            
            steps.append({
                "type": "pivot",
                "indices": [high],
                "array": arr.copy(),
                "description": f"Pivot selected: {pivot}",
                "depth": depth
            })
            
            i = low - 1
            
            for j in range(low, high):
                steps.append({
                    "type": "compare",
                    "indices": [j, high],
                    "array": arr.copy(),
                    "description": f"Comparing {arr[j]} with pivot {pivot}",
                    "depth": depth
                })
                
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    steps.append({
                        "type": "swapping",
                        "indices": [i, j],
                        "array": arr.copy(),
                        "description": f"Swapped {arr[i]} and {arr[j]}",
                        "depth": depth
                    })
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            steps.append({
                "type": "sorted",
                "indices": [i + 1],
                "array": arr.copy(),
                "description": f"Pivot {pivot} in final position {i+1}",
                "depth": depth
            })
            
            return i + 1
        
        def quick_sort_helper(arr, low, high, depth=0):
            if low < high:
                pi = partition(arr, low, high, depth)
                quick_sort_helper(arr, low, pi - 1, depth + 1)
                quick_sort_helper(arr, pi + 1, high, depth + 1)
        
        quick_sort_helper(arr, 0, len(arr) - 1)
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Quick sort completed!",
            "total_comparisons": len([s for s in steps if s["type"] == "compare"]),
            "total_swaps": len([s for s in steps if s["type"] == "swapping"])
        })
        
        return steps

    @staticmethod
    def heap_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        n = len(arr)
        
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                steps.append({
                    "type": "swapping",
                    "indices": [i, largest],
                    "array": arr.copy(),
                    "description": f"Heapifying: swapped {arr[i]} and {arr[largest]}"
                })
                heapify(arr, n, largest)
        
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            steps.append({
                "type": "sorted",
                "indices": [i],
                "array": arr.copy(),
                "description": f"Extracted {arr[i]} to position {i}"
            })
            heapify(arr, i, 0)
        
        steps.append({
            "type": "done",
            "array": arr,
            "description": "Heap sort completed!",
            "total_comparisons": 0,
            "total_swaps": len([s for s in steps if s["type"] == "swapping"])
        })
        
        return steps

    @staticmethod
    def counting_sort(arr: List[int]) -> List[Dict[str, Any]]:
        steps = []
        arr = arr.copy()
        
        if not arr:
            return steps
        
        max_val = max(arr)
        min_val = min(arr)
        range_val = max_val - min_val + 1
        count = [0] * range_val
        output = [0] * len(arr)
        
        for num in arr:
            count[num - min_val] += 1
        
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        for i in range(len(arr) - 1, -1, -1):
            output[count[arr[i] - min_val] - 1] = arr[i]
            steps.append({
                "type": "sorted",
                "indices": [count[arr[i] - min_val] - 1],
                "array": output.copy(),
                "description": f"Placed {arr[i]} at position {count[arr[i] - min_val] - 1}"
            })
            count[arr[i] - min_val] -= 1
        
        steps.append({
            "type": "done",
            "array": output,
            "description": "Counting sort completed!",
            "total_comparisons": 0,
            "total_swaps": 0
        })
        
        return steps


# ============================================================
# ENHANCED ALGORITHM METADATA WITH EDUCATION RESOURCES
# ============================================================

ALGORITHM_INFO = {
    "bubble": {
        "name": "Bubble Sort",
        "discovered": "1956",
        "also_known_as": ["Sinking Sort", "Sorting by Exchange"],
        "description": "Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they're in the wrong order. The pass through the list is repeated until the list is sorted. Named 'bubble' because smaller elements 'bubble' to the top.",
        "time_complexity": {
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
        "how_it_works": "Start from the beginning of the array. Compare each pair of adjacent elements. If the first is larger than the second, swap them. Continue until you reach the end. Repeat this process n-1 times. After each pass, the largest unsorted element 'bubbles' to its correct position at the end.",
        "code_explanation": {
            "algorithm": "Nested loops: outer loop controls passes, inner loop compares adjacent pairs. When arr[j] > arr[j+1], perform swap using tuple unpacking.",
            "key_insight": "After i passes, the last i elements are in their final sorted positions, so the inner loop range decreases each pass.",
            "optimization": "Add 'swapped' flag to detect if array is already sorted and exit early."
        },
        "real_world_uses": [
            "Educational tool for learning sorting concepts",
            "Sorting small datasets in embedded systems",
            "Bubble Tea shop - wait times (small queue sorting)",
            "Simple data ordering in games with few objects"
        ],
        "when_to_use": [
            "Learning and teaching sorting algorithms",
            "Very small datasets (n < 10)",
            "When data is nearly sorted already",
            "When simplicity is more important than efficiency"
        ],
        "when_not_to_use": [
            "Large datasets (performance is terrible)",
            "Time-critical applications",
            "Production systems",
            "Datasets in reverse order"
        ],
        "advantages": [
            "Extremely simple to understand and implement",
            "No additional memory required (in-place)",
            "Stable - maintains relative order of equal elements",
            "Can detect already-sorted arrays (with optimization)"
        ],
        "disadvantages": [
            "Very slow for large datasets",
            "Many unnecessary comparisons",
            "Poor cache performance",
            "Not used in any production systems"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/bubble-sort/",
            "youtube": "https://www.youtube.com/results?search_query=bubble+sort+algorithm+tutorial",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/sorting-algorithms",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "selection": {
        "name": "Selection Sort",
        "discovered": "1950s",
        "also_known_as": ["Simple Selection Sort"],
        "description": "Selection sort divides the array into sorted and unsorted regions. It repeatedly finds the minimum element from the unsorted region and places it at the end of the sorted region.",
        "time_complexity": {
            "best": "O(n²)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(1)",
        "stable": False,
        "in_place": True,
        "how_it_works": "Divide array into sorted (left) and unsorted (right) regions. Start with entire array unsorted. Find the minimum in unsorted region. Swap it with the first element of unsorted region. Move the boundary one element right. Repeat until array is sorted.",
        "code_explanation": {
            "algorithm": "Outer loop iterates through positions. Inner loop finds minimum from remaining unsorted elements. Swap minimum with current position.",
            "key_insight": "After i iterations, the first i elements are in their final sorted positions. Only one swap per iteration.",
            "optimization": "Minimize swaps - only swap if min_idx != i, reducing write operations."
        },
        "real_world_uses": [
            "When memory writes are expensive (limited RAM writes)",
            "Small embedded systems",
            "Sorting objects with expensive comparison functions",
            "Real-time systems with limited writes"
        ],
        "when_to_use": [
            "Small datasets (n < 20)",
            "When minimizing swaps is critical",
            "Educational purposes",
            "Memory-constrained systems"
        ],
        "when_not_to_use": [
            "Large datasets",
            "When stability is required",
            "When fewer comparisons matter",
            "When data is already sorted"
        ],
        "advantages": [
            "Minimizes number of swaps (exactly n-1 swaps maximum)",
            "Simple to implement and understand",
            "In-place sorting",
            "Predictable O(n²) in all cases",
            "Good for small lists"
        ],
        "disadvantages": [
            "Always O(n²) - not adaptive",
            "Not stable sorting algorithm",
            "Many comparisons even for sorted data",
            "Poor for large datasets"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/selection-sort/",
            "youtube": "https://www.youtube.com/results?search_query=selection+sort+algorithm",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/sorting-algorithms",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "insertion": {
        "name": "Insertion Sort",
        "discovered": "Ancient",
        "also_known_as": ["Linear Insertion Sort"],
        "description": "Insertion sort builds the final sorted array one item at a time. It takes each element and inserts it into its correct position within the already sorted portion of the array. Like sorting playing cards in your hand.",
        "time_complexity": {
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(1)",
        "stable": True,
        "in_place": True,
        "how_it_works": "Start with second element. Compare it with elements to its left. Shift larger elements one position right. Insert the element in its correct position. Repeat for each element from left to right. After processing element at position i, the first i+1 elements are sorted.",
        "code_explanation": {
            "algorithm": "Outer loop from position 1 to n. For each position, store element as key. While loop shifts larger elements right. Place key in correct position.",
            "key_insight": "Maintains a sorted prefix - all elements to the left of current position are in sorted order relative to each other.",
            "optimization": "Binary search can find insertion position (binary insertion sort) but shifting still requires O(n) operations."
        },
        "real_world_uses": [
            "Sorting playing cards by hand",
            "Library catalog systems",
            "Nearly sorted data in databases",
            "Online sorting (data arrives in real-time)",
            "Timsort algorithm (Python's default) uses insertion for small chunks"
        ],
        "when_to_use": [
            "Small datasets (n < 50)",
            "Nearly sorted data",
            "Online sorting scenarios",
            "When stability is required",
            "When you want simple, natural sorting"
        ],
        "when_not_to_use": [
            "Large random datasets",
            "Reverse-sorted data",
            "When O(n log n) is required",
            "Big data applications"
        ],
        "advantages": [
            "Efficient for small datasets",
            "Adaptive - O(n) for nearly sorted data",
            "Online - can sort as data arrives",
            "Stable sorting algorithm",
            "In-place sorting",
            "Simple implementation",
            "Natural human sorting method"
        ],
        "disadvantages": [
            "O(n²) for random or reverse-sorted data",
            "Many shifts required for unsorted data",
            "Poor cache locality",
            "Requires shifting elements"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/insertion-sort/",
            "youtube": "https://www.youtube.com/results?search_query=insertion+sort+tutorial",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/sorting-algorithms",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "merge": {
        "name": "Merge Sort",
        "discovered": "1945 by John von Neumann",
        "also_known_as": ["Mergesort"],
        "description": "Merge sort uses divide-and-conquer strategy. Divide array into halves recursively until single elements remain. Merge sorted halves back together, ensuring the result is sorted.",
        "time_complexity": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)"
        },
        "space_complexity": "O(n)",
        "stable": True,
        "in_place": False,
        "how_it_works": "Divide: Recursively split array in half until arrays of size 1 remain. Merge: Merge two sorted subarrays into one sorted array by comparing elements from each and selecting the smaller one. Repeat merging until entire array is merged back.",
        "code_explanation": {
            "algorithm": "Recursive function: if array length <= 1, return. Otherwise, find midpoint, recursively sort left half, recursively sort right half, merge the sorted halves.",
            "key_insight": "Divide-and-conquer reduces problem size logarithmically. Merging takes O(n) time, and we do it log(n) times, giving O(n log n).",
            "merge_process": "Two pointers start at beginning of left and right arrays. Compare elements, add smaller to result, advance that pointer. After one exhausts, append remaining elements."
        },
        "real_world_uses": [
            "External sorting (sorting data on disk that doesn't fit in RAM)",
            "Sorting linked lists (no random access, good for merge sort)",
            "Stable sorting requirement",
            "Java Collections.sort() uses merge sort",
            "PostgreSQL database uses merge sort",
            "Large dataset sorting in distributed systems"
        ],
        "when_to_use": [
            "Large datasets",
            "When guaranteed O(n log n) is required",
            "When stability is critical",
            "Sorting linked lists",
            "External sorting scenarios",
            "Parallel/distributed sorting"
        ],
        "when_not_to_use": [
            "Space is extremely limited",
            "Small datasets (overhead not worth it)",
            "When in-place sorting is mandatory",
            "Memory bandwidth is limited"
        ],
        "advantages": [
            "Guaranteed O(n log n) performance",
            "Stable sorting algorithm",
            "Excellent for linked lists",
            "Predictable performance",
            "Good for external sorting",
            "Highly parallelizable",
            "Works well with streaming data"
        ],
        "disadvantages": [
            "Requires O(n) extra space",
            "Not in-place sorting",
            "Slower than quicksort in practice for RAM",
            "Overhead for small datasets"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/merge-sort/",
            "youtube": "https://www.youtube.com/results?search_query=merge+sort+tutorial+divide+and+conquer",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/merge-sort",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "quick": {
        "name": "Quick Sort",
        "discovered": "1960 by Tony Hoare",
        "also_known_as": ["Quicksort", "Partition Exchange Sort"],
        "description": "Quick sort uses divide-and-conquer by selecting a pivot element and partitioning array around it. Elements smaller than pivot go left, larger go right. Recursively sort the partitions.",
        "time_complexity": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n²)"
        },
        "space_complexity": "O(log n)",
        "stable": False,
        "in_place": True,
        "how_it_works": "Select pivot (usually last element). Partition: move smaller elements to left, larger to right. Pivot is now in final position. Recursively sort left and right partitions. Performance depends on pivot choice - balanced partitions give O(n log n).",
        "code_explanation": {
            "algorithm": "Partition: use two pointers, move elements smaller than pivot left, larger right. Place pivot in correct position. Then recursively sort subarrays.",
            "key_insight": "Pivot selection is critical. Random or median-of-three pivot selection helps avoid O(n²) worst case.",
            "in_place": "No need for temporary arrays like merge sort. Partitioning done in-place by swapping."
        },
        "real_world_uses": [
            "C Standard Library qsort() uses quicksort",
            "C++ std::sort() uses introsort (quicksort hybrid)",
            "Most programming languages' default sort",
            "Database query optimization",
            "In-memory sorting of large datasets",
            "Operating system process scheduling"
        ],
        "when_to_use": [
            "General purpose sorting",
            "Large datasets in RAM",
            "When average case matters more than worst case",
            "When in-place sorting important",
            "When cache efficiency matters",
            "Most practical sorting needs"
        ],
        "when_not_to_use": [
            "Real-time systems (worst case O(n²) is risky)",
            "When stability is required",
            "When guaranteed O(n log n) is mandatory",
            "Nearly sorted data"
        ],
        "advantages": [
            "Very fast in practice (often faster than merge sort)",
            "In-place sorting (saves memory)",
            "Excellent cache locality",
            "Average O(n log n) is very good",
            "Simple elegant implementation",
            "Industry standard for general sorting"
        ],
        "disadvantages": [
            "Worst case O(n²) if bad pivot chosen",
            "Not stable sorting",
            "Recursive (uses O(log n) stack space)",
            "Performance depends on input order"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/quick-sort/",
            "youtube": "https://www.youtube.com/results?search_query=quick+sort+algorithm+tutorial",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/quick-sort",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "heap": {
        "name": "Heap Sort",
        "discovered": "1964 by J.W.J. Williams",
        "also_known_as": ["Heapsort"],
        "description": "Heap sort uses heap data structure (complete binary tree). Build max heap from array, repeatedly extract maximum element and place at end. Result is sorted array.",
        "time_complexity": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)"
        },
        "space_complexity": "O(1)",
        "stable": False,
        "in_place": True,
        "how_it_works": "Build max heap: organize array into max heap structure. Extract max: move root (maximum) to end, reduce heap size, restore heap property. Repeat until heap size is 1. Result: sorted array.",
        "code_explanation": {
            "algorithm": "Heapify: maintain max heap property where parent >= children. Build heap bottom-up from last non-leaf. Extract n-1 elements: swap root with last, heapify reduced heap.",
            "key_insight": "Heap property guarantees maximum at root. Heapify maintains this property in O(log n) time.",
            "implementation": "Stored in array: for index i, left child = 2i+1, right child = 2i+2, parent = (i-1)/2."
        },
        "real_world_uses": [
            "Priority queues in operating systems",
            "Dijkstra's algorithm for shortest paths",
            "Prim's algorithm for minimum spanning trees",
            "Huffman coding for data compression",
            "K-largest elements problem",
            "Median finding in streams"
        ],
        "when_to_use": [
            "When guaranteed O(n log n) worst case required",
            "Priority queue needs",
            "Space efficiency is critical",
            "No worst-case guarantees acceptable",
            "In-place sorting required"
        ],
        "when_not_to_use": [
            "When average case performance matters (quicksort better)",
            "When stability is required",
            "Small datasets (overhead too high)",
            "Cache efficiency critical"
        ],
        "advantages": [
            "Guaranteed O(n log n) - no worst case",
            "In-place sorting",
            "No extra space needed",
            "Good for real-time systems",
            "Foundation for priority queues",
            "No O(n²) possible"
        ],
        "disadvantages": [
            "Slower than quicksort in practice",
            "Not stable sorting",
            "Poor cache locality (random memory access)",
            "Complex implementation vs simple algorithms",
            "Hard to parallelize"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/heap-sort/",
            "youtube": "https://www.youtube.com/results?search_query=heap+sort+algorithm+tutorial",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/heap-sort",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    },
    "counting": {
        "name": "Counting Sort",
        "discovered": "Ancient (Egyptian fractions)",
        "also_known_as": ["Non-Comparison Sort"],
        "description": "Counting sort is a non-comparison algorithm. Count occurrences of each value, use counts to determine placement. Optimal when range of input is not much larger than number of elements.",
        "time_complexity": {
            "best": "O(n + k)",
            "average": "O(n + k)",
            "worst": "O(n + k)"
        },
        "space_complexity": "O(k)",
        "stable": True,
        "in_place": False,
        "how_it_works": "Find max and min values. Create count array of size (max-min+1). For each element, increment count. Calculate cumulative counts. Place elements in output array using cumulative counts. Algorithm is stable when traversing from right to left.",
        "code_explanation": {
            "algorithm": "Three phases: Count occurrences, cumulative sum of counts (gives final positions), place elements using counts.",
            "key_insight": "No comparisons needed! Uses indexing instead. Linear time possible.",
            "stability": "Traverse input from right to left and place in output from right to left to maintain order."
        },
        "real_world_uses": [
            "Radix sort subroutine",
            "Sorting integers in known range",
            "Sorting grades (0-100)",
            "Histogram generation",
            "Counting frequencies",
            "Digit DP problems",
            "Bucket sort component"
        ],
        "when_to_use": [
            "Integer sorting with known range",
            "When range k is small (k ≈ n)",
            "When O(n + k) is required",
            "Non-negative integers only",
            "Need for stability"
        ],
        "when_not_to_use": [
            "Large range of values (k >> n)",
            "Non-integer data",
            "Negative numbers (need modification)",
            "Floating point numbers",
            "When space is critical"
        ],
        "advantages": [
            "Linear time O(n + k) - theoretically optimal",
            "Stable sorting algorithm",
            "Predictable performance",
            "No comparisons needed",
            "Very fast for suitable inputs",
            "Foundation for radix sort"
        ],
        "disadvantages": [
            "Only works for integers",
            "Requires knowledge of range",
            "Extra O(k) space needed",
            "Inefficient for large ranges",
            "Cannot sort objects directly",
            "Not comparison-based"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/counting-sort/",
            "youtube": "https://www.youtube.com/results?search_query=counting+sort+algorithm+tutorial",
            "khan_academy": "https://www.khanacademy.org/computing/computer-science/algorithms/counting-sort",
            "visualgo": "https://visualgo.net/en/sorting"
        }
    }
}

# ============================================================
# CODE SNIPPETS
# ============================================================

CODE_SNIPPETS = {
    "bubble": {
        "python": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr""",
        "javascript": """function bubbleSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return arr;
}"""
    },
    "selection": {
        "python": """def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr""",
        "javascript": """function selectionSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
    }
    return arr;
}"""
    },
    "insertion": {
        "python": """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr""",
        "javascript": """function insertionSort(arr) {
    for (let i = 1; i < arr.length; i++) {
        let key = arr[i];
        let j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
    return arr;
}"""
    },
    "merge": {
        "python": """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result""",
        "javascript": """function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    return merge(left, right);
}

function merge(left, right) {
    let result = [], i = 0, j = 0;
    while (i < left.length && j < right.length) {
        result.push(left[i] <= right[j] ? left[i++] : right[j++]);
    }
    return result.concat(left.slice(i)).concat(right.slice(j));
}"""
    },
    "quick": {
        "python": """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)""",
        "javascript": """function quickSort(arr) {
    if (arr.length <= 1) return arr;
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    return [...quickSort(left), ...middle, ...quickSort(right)];
}"""
    },
    "heap": {
        "python": """def heap_sort(arr):
    def heapify(n, i):
        largest = i
        left, right = 2*i+1, 2*i+2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr""",
        "javascript": """function heapSort(arr) {
    function heapify(n, i) {
        let largest = i, left = 2*i+1, right = 2*i+2;
        if (left < n && arr[left] > arr[largest]) largest = left;
        if (right < n && arr[right] > arr[largest]) largest = right;
        if (largest !== i) {
            [arr[i], arr[largest]] = [arr[largest], arr[i]];
            heapify(n, largest);
        }
    }
    
    let n = arr.length;
    for (let i = Math.floor(n/2)-1; i >= 0; i--) heapify(n, i);
    for (let i = n-1; i > 0; i--) {
        [arr[0], arr[i]] = [arr[i], arr[0]];
        heapify(i, 0);
    }
    return arr;
}"""
    },
    "counting": {
        "python": """def counting_sort(arr):
    if not arr: return arr
    max_val, min_val = max(arr), min(arr)
    range_val = max_val - min_val + 1
    count = [0] * range_val
    output = [0] * len(arr)
    
    for num in arr:
        count[num - min_val] += 1
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    return output""",
        "javascript": """function countingSort(arr) {
    if (!arr.length) return arr;
    const max = Math.max(...arr), min = Math.min(...arr);
    const range = max - min + 1;
    const count = new Array(range).fill(0);
    const output = new Array(arr.length);
    
    arr.forEach(num => count[num - min]++);
    for (let i = 1; i < count.length; i++)
        count[i] += count[i - 1];
    for (let i = arr.length - 1; i >= 0; i--) {
        output[count[arr[i] - min] - 1] = arr[i];
        count[arr[i] - min]--;
    }
    return output;
}"""
    }
}


# ============================================================
# API ENDPOINTS
# ============================================================

@app.post("/api/sort")
async def sort_array(payload: dict = Body(...)):
    try:
        array = payload.get("array", [])
        algorithm = payload.get("algorithm", "bubble")
        
        if not array:
            raise HTTPException(status_code=400, detail="Array cannot be empty")
        
        array = [int(x) for x in array]
        start_time = time.perf_counter()
        
        if algorithm == "bubble":
            steps = SortingAlgorithms.bubble_sort(array)
        elif algorithm == "selection":
            steps = SortingAlgorithms.selection_sort(array)
        elif algorithm == "insertion":
            steps = SortingAlgorithms.insertion_sort(array)
        elif algorithm == "merge":
            steps = SortingAlgorithms.merge_sort(array)
        elif algorithm == "quick":
            steps = SortingAlgorithms.quick_sort(array)
        elif algorithm == "heap":
            steps = SortingAlgorithms.heap_sort(array)
        elif algorithm == "counting":
            steps = SortingAlgorithms.counting_sort(array)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {algorithm}")
        
        end_time = time.perf_counter()
        execution_time_us = (end_time - start_time) * 1_000_000
        
        final_step = steps[-1]
        return {
            "steps": steps,
            "execution_time_us": round(execution_time_us, 2),
            "algorithm": algorithm,
            "array_size": len(array),
            "total_comparisons": final_step.get("total_comparisons", 0),
            "total_swaps": final_step.get("total_swaps", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/algorithm-info/{algorithm}")
async def get_algorithm_info(algorithm: str):
    if algorithm not in ALGORITHM_INFO:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' not found")
    
    return ALGORITHM_INFO[algorithm]


@app.get("/api/algorithm-code/{algorithm}")
async def get_algorithm_code(algorithm: str, language: str = "python"):
    if algorithm not in CODE_SNIPPETS:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' not found")
    
    if language not in CODE_SNIPPETS[algorithm]:
        raise HTTPException(status_code=404, detail=f"Language '{language}' not available")
    
    return {
        "algorithm": algorithm,
        "language": language,
        "code": CODE_SNIPPETS[algorithm][language]
    }


@app.post("/api/time-trial")
async def time_trial(payload: dict = Body(...)):
    try:
        array = payload.get("array", [])
        
        if not array:
            raise HTTPException(status_code=400, detail="Array cannot be empty")
        
        array = [int(x) for x in array]
        algorithms = ["bubble", "selection", "insertion", "merge", "quick", "heap", "counting"]
        
        # Space complexity mapping (Big-O notation)
        space_complexity = {
            "bubble": "O(1)",
            "selection": "O(1)",
            "insertion": "O(1)",
            "merge": "O(n)",
            "quick": "O(log n)",
            "heap": "O(1)",
            "counting": "O(k)"
        }
        
        results = []
        
        for algo in algorithms:
            try:
                start_time = time.perf_counter()
                
                if algo == "bubble":
                    steps = SortingAlgorithms.bubble_sort(array)
                elif algo == "selection":
                    steps = SortingAlgorithms.selection_sort(array)
                elif algo == "insertion":
                    steps = SortingAlgorithms.insertion_sort(array)
                elif algo == "merge":
                    steps = SortingAlgorithms.merge_sort(array)
                elif algo == "quick":
                    steps = SortingAlgorithms.quick_sort(array)
                elif algo == "heap":
                    steps = SortingAlgorithms.heap_sort(array)
                elif algo == "counting":
                    steps = SortingAlgorithms.counting_sort(array)
                
                end_time = time.perf_counter()
                execution_time_us = (end_time - start_time) * 1_000_000
                final_step = steps[-1]
                
                results.append({
                    "algorithm": algo,
                    "execution_time_us": round(execution_time_us, 2),
                    "comparisons": final_step.get("total_comparisons", 0),
                    "swaps": final_step.get("total_swaps", 0),
                    "total_steps": len(steps),
                    "space_complexity": space_complexity[algo]  # ✅ Add space complexity
                })
                
            except Exception as e:
                results.append({
                    "algorithm": algo,
                    "error": str(e)
                })
        
        results.sort(key=lambda x: x.get("execution_time_us", float('inf')))
        
        return {
            "results": results,
            "array_size": len(array),
            "fastest": results[0]["algorithm"] if results else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export")
async def export_results(data: dict = Body(...)):
    export_format = data.get("format", "json")
    results = data.get("results", {})
    
    if export_format == "json":
        return JSONResponse(content=results)
    
    elif export_format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["algorithm", "array_size", "comparisons", "swaps"])
        writer.writeheader()
        writer.writerow(results)
        
        csv_content = output.getvalue()
        return JSONResponse(content={
            "csv": csv_content,
            "filename": f"sorting-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
        })
    
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {export_format}")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "3.1.0 - ULTIMATE WITH EDUCATION RESOURCES"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Ultimate Sorting Visualizer...")
    print("📍 Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
