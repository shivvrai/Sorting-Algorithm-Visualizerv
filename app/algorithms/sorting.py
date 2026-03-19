"""
Sorting Algorithms with step-by-step visualization support.
Each algorithm returns a list of step dicts for frontend animation.
"""

from typing import List, Dict, Any


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


# --- Algorithm Registry (replaces if/elif chains) ---
SORTING_REGISTRY = {
    "bubble": SortingAlgorithms.bubble_sort,
    "selection": SortingAlgorithms.selection_sort,
    "insertion": SortingAlgorithms.insertion_sort,
    "merge": SortingAlgorithms.merge_sort,
    "quick": SortingAlgorithms.quick_sort,
    "heap": SortingAlgorithms.heap_sort,
    "counting": SortingAlgorithms.counting_sort,
}
