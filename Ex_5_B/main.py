from typing import Callable, Any, Dict, List, Tuple
import output_type as out
import networkx as nx


def short_path(algorithm: Callable, graph: list, source: str, target: str, outputtype: out.OutputType = out.Route()):
    """
    Find the shortest path or distance between two nodes in a graph using a specified algorithm.

    :param algorithm: The algorithm to use for finding the shortest path. It should be a function that accepts
                      a graph, source node, and target node, and returns a tuple containing the shortest path
                      and its length.
    :param graph: The graph represented as a list of edges or a dictionary of adjacency lists.
    :param source: The source node from which to start the path.
    :param target: The target node to which to find the shortest path.
    :param outputtype: The type of output to return, either a list representing the shortest path or the
                       distance of the shortest path. Defaults to out.Route().

    :return: If outputtype is out.Route(), returns a list representing the shortest path from source to target.
             If outputtype is out.Distance(), returns the distance of the shortest path from source to target.


    >>> short_path(algorithm = dijkstra, graph = create_graph(), source = 'A', target = 'D', outputtype=out.Route())
    ['A', 'B', 'C', 'D']

    >>> short_path(algorithm = bellman_ford, graph = create_graph(), source = 'A', target = 'D', outputtype=out.Route())
    ['A', 'B', 'C', 'D']

    >>> short_path(algorithm = dijkstra, graph = create_dict_graph(), source = 'C', target = 'B', outputtype=out.Route())
    ['C', 'B']

    >>> short_path(algorithm = bellman_ford, graph = create_dict_graph(), source = 'B', target = 'A', outputtype=out.Route())
    ['B', 'A']

    >>> short_path(algorithm = dijkstra, graph = create_graph(), source = 'A', target = 'D', outputtype=out.Distance())
    4

    >>> short_path(algorithm = bellman_ford, graph = create_graph(), source = 'B', target = 'C', outputtype=out.Distance())
    2

    >>> short_path(algorithm = dijkstra, graph = create_dict_graph(), source = 'A', target = 'B', outputtype=out.Distance())
    1

    >>> short_path(algorithm = bellman_ford, graph = create_dict_graph(), source = 'A', target = 'D', outputtype=out.Distance())
    4

    """
    if isinstance(graph, dict):
        graph = transform_graph_dict_to_list(graph)

    path, distance = algorithm(graph, source, target)

    return outputtype.get_output(path, distance)


def dijkstra(graph, source, target):
    G = nx.DiGraph()
    G.add_weighted_edges_from(graph)

    shortest_path = nx.dijkstra_path(G, source=source, target=target, weight='weight')
    path_length = nx.dijkstra_path_length(G, source=source, target=target, weight='weight')

    return shortest_path, path_length


def bellman_ford(graph, source, target):
    G = nx.DiGraph()
    G.add_weighted_edges_from(graph)

    try:
        path = nx.bellman_ford_path(G, source=source, target=target, weight='weight')
        path_length = nx.bellman_ford_path_length(G, source=source, target=target, weight='weight')
        return path, path_length
    except nx.NetworkXNoPath:
        return None, float('inf')



Graph = Dict[str, List[Tuple[str, int]]]


def create_graph() -> list[tuple[str, str, int]]:
    return [
        ('A', 'B', 1),
        ('A', 'C', 4),
        ('B', 'A', 1),
        ('B', 'C', 2),
        ('B', 'D', 5),
        ('C', 'A', 4),
        ('C', 'B', 2),
        ('C', 'D', 1),
        ('D', 'B', 5),
        ('D', 'C', 1)
    ]


def create_dict_graph() -> Graph:
    return {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }


def transform_graph_dict_to_list(graph: Dict[str, List[Tuple[str, int]]]) -> List[Tuple[str, str, int]]:
    edge_list = []
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            edge_list.append((node, neighbor, weight))
    return edge_list


if __name__ == '__main__':
    import doctest

    print(doctest.testmod())
