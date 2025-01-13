import random
import networkx as nx
import math
import matplotlib.pyplot as plt
from collections import deque
from queue import PriorityQueue

class Node:
    """ Contains all data relating to individual node.

        Perform calculations: get distance to neighbors and make neighbor:distance pairs depending on graph generation logic.

    Attributes:
        x (float): X position on Cartesian plane.
        y (float): Y position on Cartesian plane.
        number (int): Node ID/identifier.
        edges (list): Edges as tuple pairs.
        neighbors (dict): Each connected neighbor (int) and their distance away (float) as key, value pairs.

    Methods:
        add_edge(edge, nodes): From graph generation logic, add edge pairs to node object list.
        update_neighbors(edge, nodes): Takes appended edges and creates neighbor dictionary with distance to each neighbor.
    """

    def __init__(self, x, y, number):
        """ Initialize class instance.
        Args:
            x (float): X position on Cartesian plane.
            y (float): Y position on Cartesian plane.
            number (int): Node ID/identifier.
        """
        self.x = x
        self.y = y
        self.number = number
        self.edges = []
        self.neighbors = {}

    def __str__(self):
        """ Print method format.

            Returns printed string detailing instance number, coordinates, edges, and neighbors.
        """

        return f"Node {self.number} at ({self.x}, {self.y}) with edges {self.edges} and neighbors {self.neighbors}"

    def add_edge(self, edge, nodes):
        """ Append edge to object attribute edges and update neighbors.

        Args:
            edge (tuple): Pair like (i, j) indicating two nodes are linked.
            nodes (list): List of Node objects to access position for later distance calculations.
        """

        self.edges.append(edge)
        self.update_neighbors(edge, nodes)

    def update_neighbors(self, edge, nodes):
        """ After edges are added based on graph generation logic, update neighbor dictionary.

            Key, value pairs of node.number and distance from self.number.

        Args:
            edge (tuple): Pair like (i, j) indicating two nodes are linked.
            nodes (list): List of Node objects to access position for later distance calculations.
        """

        for node in edge:
            if node != self.number:
                # Get distance for each edge from current node and append to neighbors dictionary {Neighbor: distance}.
                distance = calculate_distance(
                    (self.x, self.y), (nodes[node].x, nodes[node].y)
                )
                self.neighbors[node] = distance


def main():
    # Display message to user to explain the purpose.
    print("This program will create a random network graph and run Dijkstra's algorithm.")

    # Call custom_inputs to get user values to customize graph complexity.
    print("Please provide input for: ")
    n, c, s = custom_inputs()
    # n, c, s = [20, 5, 5]

    # From user input, generate n random coordinates at graph scale s.
    vertices = generate_coordinates(n, s)

    # Take generated vertices and create Node objects for each to store information.
    nodes = make_nodes(vertices)

    # Take list of nodes and complexity c and randomly form connections based on Erdos-Renyi random network generation.
    edges = generate_edges(nodes, c)

    # Pass edges to populate Node edge and neighbor list.
    make_edges(nodes, edges)

    # Loop indefinitely until the start and finish nodes are confirmed connected.
    while True:
        # Get user inputs for start and finish node numbers.
        first, last = get_destinations(n)
        # Run a breadth first search, creating a list of connected nodes.
        connected = bfs(nodes, first)
        print(f"Nodes connected to node {first}: {connected}")
        # If the finish node is connected to the start node, exit the loop.
        if last in connected:
            break
        # If not connected, ask user to try selecting a different start and stop point.
        print("Try selecting different nodes")

    # Run Dijkstra's algorithm to find shortest path from first to last node.
    neighbor_dict = shortest_path(nodes, first, last)

    # Print list of fastest path in order of nodes visited
    path = make_path(neighbor_dict, last)
    print(f"Path is {path}")

    # Calculate distance of determined path
    distance = path_distance(path, nodes)
    print(f"Distance: {round(distance, 2)} m")

    # Print start graph to visualize connections and vertices placement.
    grapher(nodes, edges, first, path)


def get_valid_input(prompt, validation_func, error_message):
    """ Helper function to validate user input.

    Args:
        prompt (str): Ask the user for some input.
        validation_func (function): Validation function such as i < x < j
        error_message (str): Output if user input is not valid.
    """

    while True:
        try:
            value = int(input(prompt))
            if validation_func(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print("Invalid input. Please enter an integer.")


def custom_inputs() -> tuple:
    """ Get node number, complexity, and scale from user.

    Returns:
        n (int): Number of nodes to generate.
        c (int): Complexity determining interconnections.
        s (int): Scale of graph.
    """

    n = get_valid_input(
        "# of vertices: ", lambda x: x > 1, "Number of vertices must be greater than 1."
    )
    c = get_valid_input(
        "1-10 for complexity: ",
        lambda x: 0 < x <= 10,
        "Complexity must be between 1 and 10.",
    )
    s = get_valid_input(
        "1-10 for scale: ", lambda x: 0 < x <= 10, "Scale must be between 1 and 10."
    )

    return n, c, s

def generate_coordinates(n: int, s: int):
    """
    Randomly generate node coordinates from user inputs.

    Args:
    n (int): number of vertices.
    s (int): scale of graph.

    Returns:
    vertices (list): list of Cartesian coordinates (x, y) for n vertices.
    """
    if n == 0:
        raise ValueError("n cannot be 0")
    vertices = []
    for _ in range(n):
        vertices.append(
            (random.randint(-(s * 10), s * 10), random.randint(-(s * 10), s * 10))
        )

    return vertices


def make_nodes(o):
    """ Takes vertices and initialize them as Node objects.

    Args:
    o (list): List of vertices

    Returns:
    nodes (list): List of Node objects.
    """

    nodes = []
    for i in range(len(o)):
        nodes.append(Node(o[i][0], o[i][1], i))
    return nodes


# Logic for edge generation used from GitHub https://lordgrilo.github.io/complexity-book/2-networkx/nb06_random_graphs.html
def generate_edges(nodes, c):
    """ Uses Erdos-Renyi random network logic for node connectedness based on a complexity factor.

    Args:
        nodes (list): List of Node objects.
        c (int): Complexity factor to determine number of edges.

    Returns:
        edges (list): Contains (i, j) like tuples for connected points.
    """

    # Initialize empty list to store edges.
    edges = []

    # Edge probability from complexity and number of nodes.
    p = (c/4) / len(nodes)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            elif [i, j] in edges or [j, i] in edges:
                continue
            elif random.random() < p:
                edges.append((i, j))
    return edges



def make_edges(nodes, edges):
    """ From list of edges, update Node object with neighbors.

    Args:
        nodes (list): List of Node objects.
        edges (list): Contains (i, j) like tuples for connected points.
    """

    for node in nodes:
        for edge in edges:
            if node.number == edge[0] or node.number == edge[1]:
                node.add_edge(edge, nodes)


def calculate_distance(coord1, coord2):
    """ Takes two Cartesian coordinates and returns the distance.

    Args:
        coord1 (tuple): X and Y coordinates as floats.
        coord2 (tuple): X and Y coordinates as floats.

    Returns:
        distance (float): Distance between coord1 and coord2
    """

    return math.dist(coord1, coord2)


def get_destinations(n):
    """ Get user start and finish destinations.

    Args:
        n (int): Number of nodes.

    Returns:
        first (int): Start node.
        last (int): End node.
    """

    first = get_valid_input(
        "First node: ", lambda x: x <= n, "Node must be in set range."
    )
    last = get_valid_input(
        "Last node: ", lambda x: x <= n, "Node must be in set range."
    )

    return first, last


def bfs(nodes, first):
    """ Breadth first search to identify what nodes are connected to the specified start node.

    Args:
        nodes (list): List of Node objects.
        first (int): Start node.

    Returns:
        result (list): Connected Node IDs/numbers in list format.

    """
    visited = set()
    queue = deque([first])
    result = []

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)
            result.append(node)

            for neighbor in nodes[node].neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
    return result


# Dijkstra's algorithm, logic used from qpwo on GitHub https://gist.github.com/qpwo/cda55deee291de31b50d408c1a7c8515
def shortest_path(nodes, first, last):
    """ Uses a uniform-cost search and PriorityQueue to find the shortest path from the first to the last node.

    Args:
        nodes (list): List of Node objects.
        first (int): Start node.
        last (int): Finish node.

    """
    visited = set()
    cost = {first: 0}
    parent = {first: None}
    todo = PriorityQueue()
    total_dist = 0
    todo.put((0, first))
    while todo:
        while not todo.empty():
            _, vertex = todo.get() # Finds lowest cost vertex
            # Loop until we get a fresh vertex
            if vertex not in visited:
                break
        else: # if todo ran out
            break # quit main loop
        visited.add(vertex)
        if vertex == last:
            break
        for neighbor in nodes[vertex].neighbors:
            distance = nodes[vertex].neighbors[neighbor]
            if neighbor in visited: continue # skip these to save time
            old_cost = cost.get(neighbor, float('inf')) # default to infinity
            new_cost = cost[vertex] + distance
            if new_cost < old_cost:
                todo.put((new_cost, neighbor))
                cost[neighbor] = new_cost
                parent[neighbor] = vertex
    return parent


# Logic taken from qpwo on GitHub https://gist.github.com/qpwo/cda55deee291de31b50d408c1a7c8515
def make_path(parent, goal):
    """ Returns the path with the lowest cost to get from the first to last node.

    Args:
        Parent (dict): Containing linked nodes.
        goal (int): Last node.

    Returns:
        path (list): Order of visited nodes to minimize travel cost.
    """
    if goal not in parent:
        return None
    v = goal
    path = []
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]


def path_distance(path, nodes):
    distance = 0
    # print(f"Path {path}")
    for i in range(len(path)-1):
        # print(f"Node {nodes[path[i]]} with neighbors {nodes[path[i]].neighbors}")
        try:
            distance += nodes[path[i]].neighbors[path[i+1]]
        except IndexError:
            pass
        # print(f"Distance {distance}")
    return distance

def grapher(nodes, e, first, path):
    """ Create NetworkX graph object and update with generated nodes and edges.

    Args:
        nodes (list): List of Node objects.
        e (list): Contains (i, j) like tuples for connected points.
    """
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.number, pos=(node.x, node.y))
    G.add_edges_from(e)
    params = {
        "node_size": 300,
        "with_labels": True,
        "edge_color": "silver",
        "node_color": ['red' if node in path else 'blue' for node in G.nodes()],
        "font_size": 12,
        "alpha": 0.7,
        "font_weight": "semibold"
    }
    print(G)
    nx.draw_networkx(
        G, pos={node.number: (node.x, node.y) for node in nodes}, hide_ticks=False, **params
    )
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("plot.png")


if __name__ == "__main__":
    main()
