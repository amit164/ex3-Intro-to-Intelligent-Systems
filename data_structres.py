# Amit Sharabai 323784298

from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.pred_dist = {}

    # function for adding edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    @staticmethod
    def get_min_path(pred, dest):
        if dest is None:
            return None
        path = []
        nexti = dest
        path.append(nexti)

        while pred[nexti] != -1:
            path.append(pred[nexti])
            nexti = pred[nexti]
        path.reverse()
        return path

    def bfs(self, src):
        if src in self.pred_dist:
            return self.pred_dist[src]
        visited = {}
        predeceddor = {}
        dist = {}
        for v in self.graph:
            visited[v] = False
            predeceddor[v] = -1
            dist[v] = 10000000
        queue = []  # Initialize a queue

        visited[src] = True
        dist[src] = 0
        queue.append(src)

        while len(queue) != 0:
            u = queue[0]
            queue.pop(0)
            for i in self.graph[u]:
                if not visited[i]:
                    visited[i] = True
                    dist[i] = dist[u] + 1
                    predeceddor[i] = u
                    queue.append(i)

        self.pred_dist[src] = (predeceddor, dist)
        return predeceddor, dist
