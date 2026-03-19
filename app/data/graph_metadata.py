"""Graph algorithm educational metadata and code snippets."""

GRAPH_ALGORITHM_INFO = {
    "bfs": {
        "name": "Breadth-First Search",
        "description": "Explores all neighbors at the current depth before moving to the next level. Uses a queue (FIFO). Guarantees shortest path in unweighted graphs.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "how_it_works": "Start from the source node and add it to a queue. While the queue is not empty: dequeue a node, mark it as visited, and enqueue all its unvisited neighbors. This level-by-level exploration ensures that each node is visited in order of increasing distance from the source.",
        "code_explanation": {
            "algorithm": "Use a queue (FIFO). Enqueue the start node. While queue is not empty, dequeue a node, process it, and enqueue all unvisited neighbors.",
            "key_insight": "BFS explores nodes level by level, so it naturally finds the shortest path in unweighted graphs.",
            "data_structure": "Queue (collections.deque in Python) ensures FIFO order for level-by-level traversal."
        },
        "real_world_uses": [
            "Shortest path in unweighted graphs (e.g., social network friend distance)",
            "Level-order traversal of trees",
            "Finding connected components",
            "Web crawlers exploring pages by depth",
            "GPS navigation with equal-cost roads",
            "Network broadcasting protocols"
        ],
        "when_to_use": [
            "Finding shortest path in unweighted graphs",
            "Level-order or breadth-first exploration needed",
            "Finding all nodes within k distance",
            "Checking if a graph is bipartite"
        ],
        "when_not_to_use": [
            "Weighted graphs (use Dijkstra instead)",
            "Very deep graphs (high memory usage)",
            "When you need to explore deep paths first"
        ],
        "advantages": [
            "Guarantees shortest path in unweighted graphs",
            "Complete — will find solution if one exists",
            "Simple and intuitive implementation",
            "Good for finding nearby nodes first"
        ],
        "disadvantages": [
            "High memory usage for wide graphs (stores entire frontier)",
            "Not optimal for weighted graphs",
            "Can be slow for very large graphs",
            "Cannot handle negative weights"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/",
            "youtube": "https://www.youtube.com/results?search_query=BFS+breadth+first+search+algorithm+tutorial",
            "visualgo": "https://visualgo.net/en/dfsbfs"
        }
    },
    "dfs": {
        "name": "Depth-First Search",
        "description": "Explores as far as possible along each branch before backtracking. Uses recursion/stack (LIFO). Fundamental for many graph problems.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "how_it_works": "Start from the source node. Visit the node, mark it as visited, then recursively visit each unvisited neighbor. When all neighbors of a node are visited, backtrack to the previous node and continue. This explores as deep as possible before going wide.",
        "code_explanation": {
            "algorithm": "Use recursion (or explicit stack). Visit node, mark visited, then recursively DFS on each unvisited neighbor. Backtrack when stuck.",
            "key_insight": "DFS uses the call stack (or explicit stack) to remember where to backtrack, exploring each branch fully before trying the next.",
            "data_structure": "Recursion stack (implicit) or explicit stack (LIFO) for iterative version."
        },
        "real_world_uses": [
            "Cycle detection in directed/undirected graphs",
            "Topological sorting (task scheduling)",
            "Path finding and maze solving",
            "Strongly connected components (Tarjan/Kosaraju)",
            "Solving puzzles (Sudoku, N-Queens)",
            "Detecting bridges and articulation points"
        ],
        "when_to_use": [
            "Cycle detection",
            "Topological sort of DAGs",
            "Exploring all paths or solutions",
            "Finding connected components",
            "Maze solving and puzzle games"
        ],
        "when_not_to_use": [
            "Finding shortest path (use BFS or Dijkstra)",
            "Very deep graphs (risk of stack overflow)",
            "When level-order traversal is needed"
        ],
        "advantages": [
            "Lower memory usage than BFS (stores only current path)",
            "Natural for recursive problems",
            "Good for detecting cycles and topological sort",
            "Simple recursive implementation"
        ],
        "disadvantages": [
            "Does not guarantee shortest path",
            "Can get stuck in infinite loops without visited tracking",
            "Risk of stack overflow for very deep graphs",
            "May explore unnecessary paths"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/",
            "youtube": "https://www.youtube.com/results?search_query=DFS+depth+first+search+algorithm+tutorial",
            "visualgo": "https://visualgo.net/en/dfsbfs"
        }
    },
    "dijkstra": {
        "name": "Dijkstra's Algorithm",
        "description": "Finds the shortest path from a source to all other vertices in a weighted graph with non-negative weights. Uses a priority queue for greedy selection.",
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "how_it_works": "Initialize all distances to infinity except source (0). Use a min-priority queue. Extract the node with smallest distance, relax all its edges: if going through this node gives a shorter path to a neighbor, update the neighbor's distance. Repeat until all nodes are processed or target is reached.",
        "code_explanation": {
            "algorithm": "Use a min-heap (priority queue). Push (0, start). Pop minimum, relax neighbors. If new_dist < current dist, update and push to heap.",
            "key_insight": "Greedy choice: always process the unvisited node with the smallest known distance. This guarantees optimality for non-negative weights.",
            "data_structure": "Min-heap (heapq in Python) for efficient extraction of the minimum-distance node."
        },
        "real_world_uses": [
            "GPS navigation and Google Maps routing",
            "Network routing protocols (OSPF)",
            "Airline flight path optimization",
            "Robotics path planning",
            "Social network proximity",
            "Telecommunications network design"
        ],
        "when_to_use": [
            "Shortest path in weighted graphs with non-negative weights",
            "Single-source shortest paths",
            "Finding shortest path between two specific nodes",
            "Network routing optimization"
        ],
        "when_not_to_use": [
            "Graphs with negative edge weights (use Bellman-Ford)",
            "Unweighted graphs (BFS is simpler and faster)",
            "All-pairs shortest paths (use Floyd-Warshall)",
            "When edge weights change dynamically"
        ],
        "advantages": [
            "Optimal — guarantees shortest path for non-negative weights",
            "Efficient with priority queue O((V+E) log V)",
            "Works for both directed and undirected graphs",
            "Can stop early when target is found",
            "Well-studied and widely implemented"
        ],
        "disadvantages": [
            "Cannot handle negative edge weights",
            "Slower than BFS for unweighted graphs",
            "Requires priority queue data structure",
            "Not ideal for dense graphs (consider Bellman-Ford)"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/",
            "youtube": "https://www.youtube.com/results?search_query=dijkstra+shortest+path+algorithm+tutorial",
            "visualgo": "https://visualgo.net/en/sssp"
        }
    },
    "prim": {
        "name": "Prim's Algorithm",
        "description": "Builds a Minimum Spanning Tree by greedily adding the cheapest edge connecting the tree to an unvisited vertex. Grows the MST from a starting node.",
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "how_it_works": "Start from any node. Add it to the MST. Among all edges connecting MST nodes to non-MST nodes, pick the one with minimum weight. Add the new node to the MST. Repeat until all nodes are in the MST. Uses a priority queue for efficient minimum edge selection.",
        "code_explanation": {
            "algorithm": "Use a min-heap. Start with (0, start_node, None). Pop minimum weight edge, add node to MST if not visited, push all edges to unvisited neighbors.",
            "key_insight": "Greedy choice: always add the cheapest edge that connects the growing MST to a new vertex. This is proven to produce the optimal MST.",
            "data_structure": "Min-heap stores (weight, node, from_node) tuples for efficient selection of the cheapest crossing edge."
        },
        "real_world_uses": [
            "Network design (minimum cable to connect all buildings)",
            "Pipeline planning (minimum pipe to connect wells)",
            "Circuit board wiring",
            "Cluster analysis in data mining",
            "Image segmentation",
            "Approximation algorithms for TSP"
        ],
        "when_to_use": [
            "Finding minimum spanning tree",
            "Dense graphs (better than Kruskal)",
            "When you need to grow MST from a specific starting point",
            "Network design problems"
        ],
        "when_not_to_use": [
            "Sparse graphs (Kruskal may be faster)",
            "Directed graphs (MST is for undirected)",
            "When you need shortest paths (use Dijkstra)",
            "Disconnected graphs"
        ],
        "advantages": [
            "Efficient for dense graphs",
            "Grows MST from a single source",
            "Works well with adjacency list + priority queue",
            "Guaranteed optimal MST"
        ],
        "disadvantages": [
            "Requires priority queue",
            "Only works for undirected connected graphs",
            "Slower than Kruskal for sparse graphs",
            "Cannot handle disconnected graphs directly"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/",
            "youtube": "https://www.youtube.com/results?search_query=prim+minimum+spanning+tree+algorithm+tutorial",
            "visualgo": "https://visualgo.net/en/mst"
        }
    },
    "kruskal": {
        "name": "Kruskal's Algorithm",
        "description": "Builds a Minimum Spanning Tree by sorting all edges and adding them if they don't create a cycle. Uses Union-Find (Disjoint Set) for cycle detection.",
        "time_complexity": "O(E log E)",
        "space_complexity": "O(V)",
        "how_it_works": "Sort all edges by weight. Initialize each vertex as its own component. Iterate through edges in order: if the two vertices are in different components, add the edge to the MST and merge their components using Union-Find. Skip edges that would create a cycle (same component). Stop when MST has V-1 edges.",
        "code_explanation": {
            "algorithm": "Sort edges by weight. Use Union-Find: find(x) returns root, union(a,b) merges components. For each edge, if find(u) != find(v), add to MST and union.",
            "key_insight": "Sorting edges + Union-Find cycle detection. Path compression and union by rank make find/union nearly O(1) amortized.",
            "data_structure": "Union-Find (Disjoint Set Union) with path compression and union by rank for near-constant time operations."
        },
        "real_world_uses": [
            "Network design (connecting cities with minimum total road)",
            "Clustering (remove longest edges to get clusters)",
            "Image segmentation (merge similar pixels)",
            "Approximation for Steiner tree problem",
            "Pipeline and cable layout optimization",
            "Minimum cost network connections"
        ],
        "when_to_use": [
            "Finding minimum spanning tree",
            "Sparse graphs (edges already available as list)",
            "When edges are naturally given as a list",
            "Clustering by removing MST edges"
        ],
        "when_not_to_use": [
            "Dense graphs (Prim may be faster)",
            "When growing MST from a specific start point matters",
            "Directed graphs",
            "When you need shortest paths"
        ],
        "advantages": [
            "Simple and intuitive approach",
            "Efficient for sparse graphs O(E log E)",
            "Easy to implement with Union-Find",
            "Guaranteed optimal MST",
            "Works well when edge list is available"
        ],
        "disadvantages": [
            "Requires sorting all edges first",
            "Slower than Prim for dense graphs",
            "Needs Union-Find data structure",
            "Only works for undirected connected graphs"
        ],
        "resources": {
            "geeksforgeeks": "https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/",
            "youtube": "https://www.youtube.com/results?search_query=kruskal+minimum+spanning+tree+algorithm+tutorial",
            "visualgo": "https://visualgo.net/en/mst"
        }
    }
}


GRAPH_CODE_SNIPPETS = {
    "bfs": {
        "python": """from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order"""
    },
    "dfs": {
        "python": """def dfs(graph, start):
    visited = set()
    order = []

    def helper(node):
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                helper(neighbor)

    helper(start)
    return order"""
    },
    "dijkstra": {
        "python": """import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {}
    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node].items():
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))
    return dist, prev"""
    },
    "prim": {
        "python": """import heapq

def prim(graph, start):
    visited = set()
    mst_edges = []
    total = 0
    pq = [(0, start, None)]

    while pq:
        weight, node, frm = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if frm is not None:
            mst_edges.append((frm, node, weight))
            total += weight
        for neighbor, w in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (w, neighbor, node))
    return mst_edges, total"""
    },
    "kruskal": {
        "python": """def kruskal(graph):
    parent, rank = {}, {}
    for node in graph:
        parent[node] = node
        rank[node] = 0

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        if rank[ra] < rank[rb]: ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]: rank[ra] += 1
        return True

    edges = []
    seen = set()
    for u in graph:
        for v, w in graph[u].items():
            key = (min(u,v), max(u,v))
            if key not in seen:
                edges.append((w, u, v))
                seen.add(key)
    edges.sort()

    mst, total = [], 0
    for w, u, v in edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
    return mst, total"""
    }
}
