"""
Graph Algorithms with step-by-step visualization support.
Each algorithm returns a list of step dicts for frontend animation.
"""

import heapq
from collections import deque
from typing import Dict, Any, Optional, List


class GraphAlgorithms:

    @staticmethod
    def bfs(graph, start, directed):
        steps = []
        visited = set()
        queue = deque([start])
        visited.add(start)
        order = []

        steps.append({
            "type": "start",
            "current": start,
            "visited": [start],
            "queue": list(queue),
            "edges": [],
            "description": f"Starting BFS from node {start}. Add {start} to queue."
        })

        while queue:
            node = queue.popleft()
            order.append(node)

            steps.append({
                "type": "visit",
                "current": node,
                "visited": list(visited),
                "queue": list(queue),
                "edges": [],
                "description": f"Dequeued and visiting node {node}"
            })

            neighbors = sorted(graph.get(node, {}).keys())
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    steps.append({
                        "type": "explore_edge",
                        "current": node,
                        "neighbor": neighbor,
                        "visited": list(visited),
                        "queue": list(queue),
                        "edges": [[node, neighbor]],
                        "description": f"Discovered {neighbor} via {node} → {neighbor}. Added to queue."
                    })
                else:
                    steps.append({
                        "type": "skip",
                        "current": node,
                        "neighbor": neighbor,
                        "visited": list(visited),
                        "queue": list(queue),
                        "edges": [[node, neighbor]],
                        "description": f"Node {neighbor} already visited, skipping."
                    })

        steps.append({
            "type": "done",
            "visited": list(visited),
            "description": f"BFS complete! Traversal order: {' → '.join(order)}"
        })
        return steps

    @staticmethod
    def dfs(graph, start, directed):
        steps = []
        visited = set()
        order = []

        steps.append({
            "type": "start",
            "current": start,
            "visited": [],
            "edges": [],
            "description": f"Starting DFS from node {start}"
        })

        def dfs_helper(node):
            visited.add(node)
            order.append(node)

            steps.append({
                "type": "visit",
                "current": node,
                "visited": list(visited),
                "edges": [],
                "description": f"Visiting node {node} (depth: {len(order)})"
            })

            neighbors = sorted(graph.get(node, {}).keys())
            for neighbor in neighbors:
                if neighbor not in visited:
                    steps.append({
                        "type": "explore_edge",
                        "current": node,
                        "neighbor": neighbor,
                        "visited": list(visited),
                        "edges": [[node, neighbor]],
                        "description": f"Exploring edge {node} → {neighbor}"
                    })
                    dfs_helper(neighbor)
                    steps.append({
                        "type": "backtrack",
                        "current": node,
                        "visited": list(visited),
                        "edges": [],
                        "description": f"Backtracking to node {node}"
                    })
                else:
                    steps.append({
                        "type": "skip",
                        "current": node,
                        "neighbor": neighbor,
                        "visited": list(visited),
                        "edges": [[node, neighbor]],
                        "description": f"Node {neighbor} already visited, skipping."
                    })

        dfs_helper(start)

        steps.append({
            "type": "done",
            "visited": list(visited),
            "description": f"DFS complete! Traversal order: {' → '.join(order)}"
        })
        return steps

    @staticmethod
    def dijkstra(graph, start, directed, target=None):
        steps = []
        dist = {node: float('inf') for node in graph}
        dist[start] = 0
        visited = set()
        prev = {}
        pq = [(0, start)]

        target_msg = f" to target {target}" if target else ""
        steps.append({
            "type": "start",
            "current": start,
            "distances": {k: v if v != float('inf') else "∞" for k, v in dist.items()},
            "visited": [],
            "edges": [],
            "description": f"Starting Dijkstra from node {start}{target_msg}. Distance to {start} = 0, all others = ∞"
        })

        while pq:
            d, node = heapq.heappop(pq)
            if node in visited:
                continue

            visited.add(node)
            steps.append({
                "type": "visit",
                "current": node,
                "distances": {k: v if v != float('inf') else "∞" for k, v in dist.items()},
                "visited": list(visited),
                "edges": [[prev.get(node), node]] if node in prev else [],
                "description": f"Visiting node {node} with distance {d}"
            })

            # Early termination if target reached
            if target and node == target:
                # Reconstruct path
                path = []
                cur = target
                while cur is not None:
                    path.append(cur)
                    cur = prev.get(cur)
                path.reverse()
                path_edges = [[path[i], path[i+1]] for i in range(len(path)-1)]
                final_distance = int(d) if d == int(d) else d
                steps.append({
                    "type": "done",
                    "distances": {k: v if v != float('inf') else "∞" for k, v in dist.items()},
                    "visited": list(visited),
                    "path": path,
                    "path_edges": path_edges,
                    "target": target,
                    "final_distance": final_distance,
                    "description": f"✅ Shortest path from {start} → {target}: {' → '.join(path)} | Total distance: {final_distance}"
                })
                return steps

            neighbors = graph.get(node, {})
            for neighbor, weight in neighbors.items():
                new_dist = d + weight
                steps.append({
                    "type": "explore_edge",
                    "current": node,
                    "neighbor": neighbor,
                    "weight": weight,
                    "distances": {k: v if v != float('inf') else "∞" for k, v in dist.items()},
                    "visited": list(visited),
                    "edges": [[node, neighbor]],
                    "description": f"Edge {node} → {neighbor} (weight {weight}). New distance = {d} + {weight} = {new_dist}"
                })

                if new_dist < dist[neighbor]:
                    old_dist = dist[neighbor]
                    dist[neighbor] = new_dist
                    prev[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))
                    steps.append({
                        "type": "relax",
                        "current": node,
                        "neighbor": neighbor,
                        "distances": {k: v if v != float('inf') else "∞" for k, v in dist.items()},
                        "visited": list(visited),
                        "edges": [[node, neighbor]],
                        "description": f"Relaxed {neighbor}: {old_dist if old_dist != float('inf') else '∞'} → {new_dist}"
                    })

        final_dist = {k: v if v != float('inf') else "∞" for k, v in dist.items()}
        if target:
            steps.append({
                "type": "done",
                "distances": final_dist,
                "visited": list(visited),
                "target": target,
                "description": f"❌ Dijkstra complete! Target {target} is unreachable from {start}."
            })
        else:
            dist_summary = ", ".join(f"{k}: {v}" for k, v in sorted(final_dist.items()))
            steps.append({
                "type": "done",
                "distances": final_dist,
                "visited": list(visited),
                "description": f"✅ Dijkstra complete! Shortest distances from {start} → {{ {dist_summary} }}"
            })
        return steps

    @staticmethod
    def prim(graph, start, directed):
        steps = []
        visited = set()
        mst_edges = []
        total_weight = 0
        pq = [(0, start, None)]  # (weight, node, from_node)

        steps.append({
            "type": "start",
            "current": start,
            "visited": [],
            "mst_edges": [],
            "edges": [],
            "description": f"Starting Prim's MST from node {start}"
        })

        while pq:
            weight, node, from_node = heapq.heappop(pq)
            if node in visited:
                continue

            visited.add(node)
            if from_node is not None:
                mst_edges.append([from_node, node, weight])
                total_weight += weight

            steps.append({
                "type": "visit",
                "current": node,
                "from_node": from_node,
                "weight": weight,
                "visited": list(visited),
                "mst_edges": [e[:2] for e in mst_edges],
                "edges": [[from_node, node]] if from_node else [],
                "description": f"Adding node {node} to MST" + (f" via edge {from_node}→{node} (weight {weight})" if from_node else "")
            })

            neighbors = graph.get(node, {})
            for neighbor, w in neighbors.items():
                if neighbor not in visited:
                    heapq.heappush(pq, (w, neighbor, node))
                    steps.append({
                        "type": "explore_edge",
                        "current": node,
                        "neighbor": neighbor,
                        "weight": w,
                        "visited": list(visited),
                        "mst_edges": [e[:2] for e in mst_edges],
                        "edges": [[node, neighbor]],
                        "description": f"Edge {node}→{neighbor} (weight {w}) added to priority queue"
                    })

        steps.append({
            "type": "done",
            "visited": list(visited),
            "mst_edges": [e[:2] for e in mst_edges],
            "total_weight": total_weight,
            "description": f"Prim's MST complete! Total weight: {total_weight}"
        })
        return steps

    @staticmethod
    def kruskal(graph, start, directed):
        steps = []
        parent = {}
        rank = {}

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
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        # Collect all edges
        edges = []
        seen = set()
        for u in graph:
            for v, w in graph[u].items():
                key = (min(u, v), max(u, v))
                if key not in seen:
                    edges.append((w, u, v))
                    seen.add(key)
        edges.sort()

        steps.append({
            "type": "start",
            "visited": list(graph.keys()),
            "mst_edges": [],
            "edges": [],
            "description": f"Starting Kruskal's MST. {len(edges)} edges sorted by weight."
        })

        mst_edges = []
        total_weight = 0

        for w, u, v in edges:
            steps.append({
                "type": "explore_edge",
                "current": u,
                "neighbor": v,
                "weight": w,
                "visited": list(graph.keys()),
                "mst_edges": [e[:2] for e in mst_edges],
                "edges": [[u, v]],
                "description": f"Considering edge {u}→{v} (weight {w})"
            })

            if find(u) != find(v):
                union(u, v)
                mst_edges.append([u, v, w])
                total_weight += w
                steps.append({
                    "type": "add_edge",
                    "current": u,
                    "neighbor": v,
                    "weight": w,
                    "visited": list(graph.keys()),
                    "mst_edges": [e[:2] for e in mst_edges],
                    "edges": [[u, v]],
                    "description": f"Added edge {u}→{v} (weight {w}) to MST. Total: {total_weight}"
                })
            else:
                steps.append({
                    "type": "reject_edge",
                    "current": u,
                    "neighbor": v,
                    "weight": w,
                    "visited": list(graph.keys()),
                    "mst_edges": [e[:2] for e in mst_edges],
                    "edges": [[u, v]],
                    "description": f"Rejected edge {u}→{v} (would create cycle)"
                })

        steps.append({
            "type": "done",
            "visited": list(graph.keys()),
            "mst_edges": [e[:2] for e in mst_edges],
            "total_weight": total_weight,
            "description": f"Kruskal's MST complete! Total weight: {total_weight}"
        })
        return steps


# --- Algorithm Registry ---
GRAPH_REGISTRY = {
    "bfs": lambda graph, start, directed, **kw: GraphAlgorithms.bfs(graph, start, directed),
    "dfs": lambda graph, start, directed, **kw: GraphAlgorithms.dfs(graph, start, directed),
    "dijkstra": lambda graph, start, directed, **kw: GraphAlgorithms.dijkstra(graph, start, directed, target=kw.get("target")),
    "prim": lambda graph, start, directed, **kw: GraphAlgorithms.prim(graph, start, directed),
    "kruskal": lambda graph, start, directed, **kw: GraphAlgorithms.kruskal(graph, start, directed),
}
