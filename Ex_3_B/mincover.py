import subprocess, sys
import networkx as nx, cvxpy as cp, numpy as np, matplotlib.pyplot as plt
from networkx.algorithms.approximation import min_weighted_vertex_cover

subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxopt"], stdout=subprocess.DEVNULL)


def mincover(graph: nx.Graph) -> int:
    # Number of nodes
    n = len(graph.nodes)

    # Create a binary variable for each node
    x = cp.Variable(n, boolean=True)

    # Create the constraints: for each edge (u, v), u or v (or both) must be in the cover
    constraints = []
    for u, v in graph.edges():
        constraints.append(x[u] + x[v] >= 1)

    # The objective is to minimize the sum of the binary variables
    objective = cp.Minimize(cp.sum(x))

    # Formulate the problem
    problem = cp.Problem(objective, constraints)

    # Solve the problem
    problem.solve(solver=cp.CBC)  # Use the CBC solver for integer programming

    # The optimal value of the objective function is the size of the minimum vertex cover
    return int(problem.value)


def test_mincover():
    # Test with a simple triangle graph
    triangle = nx.Graph([(0, 1), (1, 2), (2, 0)])
    assert mincover(triangle) == 2, "Test case 1 failed"

    # Test with a simple square graph
    k_4 = nx.Graph([(0, 1), (0, 2), (0, 3),
                    (1, 2), (1, 3),
                    (2, 3)])
    assert mincover(k_4) == 3, "Test case 2 failed"

    k_7 = nx.Graph([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                    (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                    (2, 3), (2, 4), (2, 5), (2, 6),
                    (3, 4), (3, 5), (3, 6),
                    (4, 5), (4, 6),
                    (5, 6)])
    assert mincover(k_7) == 6, "Test case 3 failed"

    rand_nodes = np.random.randint(1, 51)
    # Create the complete graph (clique graph) with n nodes
    k_n = nx.complete_graph(rand_nodes)
    assert mincover(k_n) == rand_nodes-1, "Test case 4 failed"

    # Test with a larger random graph
    np.random.seed(42)
    for n in range(10, 51, 10):  # Test with graphs of sizes 10, 20, 30, 40, and 50
        G = nx.gnm_random_graph(n, 10 * n)  # Generate a random graph with approximately 10*n edges
        result = mincover(G)
        expected = len(nx.min_weighted_vertex_cover(G))
        assert result <= expected, "Test case 5 failed"


if __name__ == '__main__':
    # edges = eval(input())
    # graph = nx.Graph(edges)
    # print(mincover(graph))

    # G = nx.Graph([(0, 1), (1, 2), (2, 0), (1, 3), (1, 4), (1, 5)])
    # k_7 = nx.Graph([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    #                 (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
    #                 (2, 3), (2, 4), (2, 5), (2, 6),
    #                 (3, 4), (3, 5), (3, 6),
    #                 (4, 5), (4, 6),
    #                 (5, 6)])
    # print(mincover(G))

    # triangle = nx.Graph([(0, 1), (1, 2), (2, 0)])
    # k_4 = nx.Graph([(0, 1), (0, 2), (0, 3),
    #                 (1, 2), (1, 3),
    #                 (2, 3)])
    # print(mincover(k_4))
    # print(min_weighted_vertex_cover(k_4))

    test_mincover()
