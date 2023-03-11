import pygame
import numpy as np
import heapq

from math import dist
from utils import flatten
from settings import *


class Node:
    """
    Node that will construct the grid and will be given information
    so that the heuristics can be calculated
    """

    def __init__(self, i: int, j: int):

        # Initialise the coordinates
        self.i = i
        self.j = j

        # Initialise the heuristic variables
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0

        # Set the board parameters
        self.start = False
        self.end = False
        self.obstruction = False

        # Variable for the parent node
        self.parent = None
        self.path = False

        # Give the node a rect variable so that it can interact
        self.rect = None

    def __eq__(self, __o) -> bool:
        return (self.i == __o.i) and (self.j == __o.j)

    def __ne__(self, __o) -> bool:
        return not (self == __o)

    # Created only for Djikstra implementation
    def __lt__(self, __o) -> bool:
        return True

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def draw(self, board_origin: int, cell_size: int, screen: pygame.Surface) -> None:
        """Method that draws the rect for each node."""
        self.rect = pygame.Rect(
            board_origin[0] + self.j * cell_size,
            board_origin[1] + self.i * cell_size,
            cell_size,
            cell_size,
        )
        pygame.draw.rect(screen, WHITE, self.rect, 1)

    def fill(self, screen: pygame.Surface, colour: tuple) -> None:
        """Fills the rect of the node with a certain colour."""
        pygame.draw.rect(screen, colour, self.rect)

    def coords(self):
        return (self.i, self.j)


class Grid:
    """The grid, constructed of Node objects, that the visualiser will traverse."""

    def __init__(self, height, width, board_origin, cell_size, pin, flag):

        # Set the variables for the board
        self.height = height
        self.width = width

        self.board_origin = board_origin
        self.cell_size = cell_size
        self.screen = pygame.display.get_surface()
        self.pin = pin
        self.flag = flag

        # Create the grid
        self.cells = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Node(i, j))
            self.cells.append(row)

        self.start = None
        self.end = None

        # Set frontier and searched
        self.open = []
        self.closed = []

    def generate_maze(self, mask: np.ndarray) -> None:
        """Randomly generates a maze on the GUI"""

        for i, row in enumerate(self.cells):
            for j, node in enumerate(row):
                if mask[i][j] == 1:
                    node.obstruction = True

    def get_neigbours(self, node: Node) -> list:
        """
        Returns a set of nodes that are vertically, horizontally, and diagonally adjacent to the node.
        """
        neighbours = []

        for i in range(node.i - 1, node.i + 2):
            for j in range(node.j - 1, node.j + 2):

                # Check it falls within the grid
                if 0 <= i < self.height and 0 <= j < self.width:

                    # Define a Node variable called neighbour
                    neighbour = self.cells[i][j]

                    # Ignore the cell itself
                    if neighbour != node and not neighbour.obstruction:
                        neighbours.append(neighbour)

        return neighbours

    def g_heuristic(self, node: Node) -> None:
        """
        Calculates the Manhattan distance for the greedy algorithm
        and assigns it to the node.g variable.
        """
        node.h = abs(node.i - self.end.i) + abs(node.j - self.end.j)

    def weight(self, parent: Node, child: Node) -> float:
        """Returns the euclidean distance between two nodes"""
        return np.sqrt((parent.i - child.i) ** 2 + (parent.j - child.j) ** 2)

    def draw_board(self) -> None:
        """Updates the board and the colours of the rects"""
        for row in self.cells:
            for node in row:
                node.draw(self.board_origin, self.cell_size, self.screen)

                if node.obstruction:
                    node.fill(self.screen, WHITE)
                elif node.start:
                    self.screen.blit(self.pin, node.rect)
                elif node.end:
                    self.screen.blit(self.flag, node.rect)
                elif node in self.closed:
                    node.fill(self.screen, RED)
                elif node in self.open:
                    node.fill(self.screen, GREEN)

    def asearch(self) -> bool:
        """A* search algorithm."""

        # Append the starting node to the open list
        self.open.append(self.start)

        while self.open:

            # Set the current node to the node with the smallest f value
            current = self.open[0]
            current_index = 0
            for index, node in enumerate(self.open):
                if node.f < current.f:
                    current = node
                    current_index = index

            # Remove current from the grid.open
            self.open.pop(current_index)

            # Append current to grid.closed
            self.closed.append(current)

            # Check current node is the goal
            if current == self.end:

                # Break while loop
                return True

            # Generate the neighbours
            neighbours = self.get_neigbours(current)

            for neighbour in neighbours:

                # Check whether neighbour has been searched
                if neighbour in self.closed:
                    continue

                tentative_g_score = current.g + dist(
                    current.coords(), neighbour.coords()
                )

                if neighbour not in self.open:

                    self.open.append(neighbour)
                    h = dist(neighbour.coords(), self.end.coords())
                    neighbour.f = tentative_g_score + h
                    neighbour.g = tentative_g_score

                    # Assign parent
                    neighbour.parent = current

                elif tentative_g_score < neighbour.g:
                    neighbour.g = tentative_g_score
                    neighbour.f = tentative_g_score + dist(
                        neighbour.coords(), self.end.coords()
                    )

            # Draw the board
            self.draw_board()

            pygame.display.update()

        # If open no longer has nodes
        return False

    def djikstra(self):
        """Djikstra's algorithm."""
        distances = {node: float("inf") for node in flatten(self.cells)}
        distances[self.start] = 0
        visited = self.closed

        # Use a priority queue to keep track of the next node to vist
        queue = [(0, self.start)]

        while queue:
            # Get the node with the smallest distance from the start node
            current_distance, current_node = heapq.heappop(queue)

            # Skip ndoes that have already been visited
            if current_node in visited:
                continue

            # Mark the current node as visited
            visited.append(current_node)

            # Check if reached end
            if current_node == self.end:
                return True

            for neighbour in self.get_neigbours(current_node):
                distance = dist(self.end.coords(), neighbour.coords())
                new_distance = current_distance + distance
                if new_distance < distances[neighbour]:
                    neighbour.parent = current_node
                    distances[neighbour] = new_distance
                    heapq.heappush(queue, (new_distance, neighbour))

            self.draw_board()
            pygame.display.update()

        # Search unsuccessful
        return False

    def bfs(self, board_origin, cell_size, screen, pin, flag) -> bool:
        """
        Breadth first search algorithm, using the open and closed list
        as the queue and visited list
        """
        visited = self.closed
        queue = self.open

        # Add the starting node to the visited and queue
        queue.append(self.start)
        visited.append(self.start)

        while queue:

            # Pop the first element in the queue
            current = queue.pop(0)

            # Get the nodes neighbours
            neighbours = self.get_neigbours(current)

            for neighbour in neighbours:

                if not neighbour.parent:
                    neighbour.parent = current

                # Check that neighbour is not in visited:
                if neighbour not in visited:

                    # Mark the node as visited
                    visited.append(neighbour)

                    # Check if it's the goal node
                    if neighbour == self.end:
                        return True

                    # Else append it to the queue
                    else:
                        queue.append(neighbour)

            # Draw the board
            self.draw_board()

            pygame.display.update()

        # Search unsuccessful
        return False

    def dfs(self) -> bool:
        """
        Depth-First Search where the set of visited is self.closed
        and the stack is self.open
        """
        # Initialise visited and stack
        visited = self.closed
        stack = self.open

        # Append the start node to the stack
        stack.append(self.start)

        # Initiate loop
        while stack:

            # Pop the element from the stack and append it to the visited
            current = stack.pop()

            # Mark the node as visited
            if current not in visited:
                visited.append(current)

            # Generate the neighbours of the node
            neighbours = self.get_neigbours(current)

            for neighbour in neighbours:

                if not neighbour.parent:
                    neighbour.parent = current

                # Check the node is not in visited
                if neighbour not in visited:

                    # Check the node is the end
                    if neighbour == self.end:
                        return True

                    else:
                        stack.append(neighbour)

            # Draw the board
            self.draw_board()

            pygame.display.update()

        # Search unsucessful
        return False

    def greedy(self) -> bool:
        """
        Greedy pathfinding algorithm that uses self.open and self.closed
        as the two main lists
        """

        # Calculate the heuristic for the starting node
        self.g_heuristic(self.start)

        # Append the node to the open list
        self.open.append(self.start)

        while self.open:

            # Find the node with the minimum heuristic value
            current = self.open[0]
            current_idx = 0

            for index, node in enumerate(self.open):
                if node.g < current.g:
                    current = node
                    current_idx = index

            # Remove this node from the open list
            current = self.open.pop(current_idx)

            # Check whether current node is the end
            if current == self.end:
                return True

            # Append current node to the closed list
            self.closed.append(current)

            # Generate the neighbours of the current node
            neighbours = self.get_neigbours(current)

            for neighbour in neighbours:

                # Calculate the heuristic value for the neighbour
                self.g_heuristic(neighbour)

                # Set the parent
                if neighbour not in self.closed and neighbour not in self.open:

                    # Set the parent
                    neighbour.parent = current

                    # Add the neighbour to the open list
                    self.open.append(neighbour)

                elif neighbour in self.open:

                    continue

            # Draw the board
            self.draw_board()

            pygame.display.update()

        # Search unsuccessful
        return False

    def find_path(self) -> None:
        """Marks nodes as belonging to the path."""

        current = self.end

        while current != self.start:
            current.path = True
            current = current.parent
