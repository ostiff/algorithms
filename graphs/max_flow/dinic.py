from collections import deque


class Dinic:
    level_graph = None
    capacity_graph = None
    flow_graph = None

    def __init__(self, graph):
        self.INF_FLOW = int(2 ** 31 - 1)
        self.n_vertices = len(graph) + 2
        self.graph = graph

    def bfs(self):
        """
        Create a level graph using the object's current flow and capacity graphs.
        """

        q = deque([0])

        self.level_graph = [-1] * self.n_vertices
        self.level_graph[0] = 0

        while q:
            curr_vertex = q.popleft()

            for i in range(self.n_vertices):
                if (self.level_graph[i] == -1
                        and self.flow_graph[curr_vertex][i] < self.capacity_graph[curr_vertex][i]):
                    q.append(i)
                    self.level_graph[i] = self.level_graph[curr_vertex] + 1

        return self.level_graph[-1] >= 0

    def dfs(self, curr_vertex, curr_flow):
        """
        Augment the flow.
        """

        if curr_vertex == self.n_vertices - 1:
            return curr_flow

        for i in range(self.n_vertices):
            if ((self.level_graph[i] == self.level_graph[curr_vertex] + 1)
                    and (self.flow_graph[curr_vertex][i] < self.capacity_graph[curr_vertex][i])):

                new_flow = min(curr_flow, self.capacity_graph[curr_vertex][i]
                               - self.flow_graph[curr_vertex][i])
                temp_flow = self.dfs(i, new_flow)

                if temp_flow > 0:
                    self.flow_graph[curr_vertex][i] += temp_flow
                    self.flow_graph[i][curr_vertex] -= temp_flow

                    return temp_flow

        return 0

    def make_consolidated(self, sources, sinks):
        """
        Make input graph into a consolidated graph with only one source and one sink.
        """

        network_graph = [[0] * self.n_vertices]

        for row in self.graph:
            network_graph.append([0] + row + [0])

        network_graph.append([0] * self.n_vertices)

        for en in sources:
            network_graph[0][en + 1] = self.INF_FLOW

        for ex in sinks:
            network_graph[ex + 1][self.n_vertices - 1] = self.INF_FLOW

        return network_graph

    def get_max_flow(self, sources, sinks):
        """
        Get the maximum flow through the graph.
        """

        self.flow_graph = [[0] * self.n_vertices for _ in range(self.n_vertices)]
        self.capacity_graph = self.make_consolidated(sources, sinks)

        max_flow = 0
        while self.bfs():
            max_flow += self.dfs(0, self.INF_FLOW)

        return max_flow


def example_1():
    G = [[0, 0, 6, 4, 0, 0],
         [0, 0, 2, 5, 0, 0],
         [0, 0, 0, 0, 6, 6],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

    print("Graph: G[u][v] = capacity")
    print('\n'.join([''.join(['{:6}'.format(u) for u in row])
                     for row in G]))

    dinic = Dinic(G)

    sources = [0, 1]
    sinks = [4, 5]
    print(f"Sources: {sources}; Sinks: {sinks}; Max flow: {dinic.get_max_flow(sources, sinks)}")

    sources = [1]
    sinks = [3, 5]
    print(f"Sources: {sources}; Sinks: {sinks}; Max flow: {dinic.get_max_flow(sources, sinks)}")


if __name__ == '__main__':
    example_1()
