"""Sorting algorithm educational metadata."""

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
