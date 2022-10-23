import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node():
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
        self.g =  0.0
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
    
    
    def __eq__(self, __o: object) -> bool:
        return (
            (self.i == __o.i) and
            (self.j == __o.j)
        )

    
    def draw(self, i: int, j: int, board_origin: int, cell_size: int, screen: pygame.Surface) -> None:
        """Method that draws the rect for each node."""
        self.rect = pygame.Rect(
            board_origin[0] + j * cell_size,
            board_origin[1] + i * cell_size,
            cell_size, cell_size
        )
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        

    def fill(self, screen: pygame.Surface, colour: tuple) -> None:
        """Fills the rect of the node with a certain colour."""
        pygame.draw.rect(screen, colour, self.rect)


class Grid():
    """The grid, constructed of Node objects, that the visualiser will traverse."""

    def __init__(self, height: int=25, width: int=40):
        
        # Set the variables for the board
        self.height = height
        self.width = width

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
    
    
    def a_heuristics(self, parent: Node, node: Node) -> None:
        """
        Calculates the g, h, and f values for a node using Eucliadian distance. The g value calculates
        the distance from the starting node to the current node. The h value calculates the distance from
        the starting node to the end node. The f value combines these two for the final cost of the move.
        """
        node.g = (parent.i - node.i) ** 2 + (parent.j - node.j) ** 2
        node.h = (self.end.i - node.i) ** 2 + (self.end.j - node.j) ** 2
        node.f = node.g + node.h

    
    def g_heuristic(self, node: Node) -> None:
        """
        Calculates the Manhattan distance for the greedy algorithm
        and assigns it to the node.g variable.
        """
        node.h = abs(node.i - self.end.i) + abs(node.j - self.end.j)

    
    def draw_board(self, board_origin, cell_size, screen, pin, flag) -> None:
        """Updates the board and the colours of the rects"""
        for row in self.cells:
            for node in row:
                i = node.i
                j = node.j
                node.draw(i, j, board_origin, cell_size, screen)

                if node.obstruction:
                    node.fill(screen, WHITE)
                elif node.start:
                    screen.blit(pin, node.rect)
                elif node.end:
                    screen.blit(flag, node.rect)
                elif node in self.closed:
                    node.fill(screen, RED)
                elif node in self.open:
                    node.fill(screen, GREEN)


    def check_neighbour(self, neighbour: Node) -> bool:
        for open_neighbour in self.open:
            if neighbour == open_neighbour and neighbour.g > open_neighbour.g:
                return True

    
    def asearch(self, board_origin, cell_size, screen, pin, flag) -> bool:
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

                # Check if neighbour already on the open list
                if self.check_neighbour(neighbour):
                    continue

                # Calculate the heuristic values
                self.a_heuristics(current, neighbour)
                
                self.open.append(neighbour)            

                # Assign parent
                neighbour.parent = current

            # Draw the board
            self.draw_board(board_origin, cell_size, screen, pin, flag)

            pygame.display.update()

        # If open no longer has nodes
        return False

    
    def djikstra(self):
        raise NotImplementedError
    
    
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
            self.draw_board(board_origin, cell_size, screen, pin, flag)

            pygame.display.update()

        # Search unsuccessful
        return False
    
    
    def dfs(self, board_origin, cell_size, screen, pin, flag) -> bool:
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
            self.draw_board(board_origin, cell_size, screen, pin, flag)

            pygame.display.update()

        # Search unsucessful
        return False

    
    def greedy(self, board_origin, cell_size, screen, pin, flag) -> bool:
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
            self.draw_board(board_origin, cell_size, screen, pin, flag)

            pygame.display.update()

        # Search unsuccessful
        return False


    def find_path(self) -> None:
        """Marks nodes as belonging to the path."""

        current = self.end

        while current != self.start:
            current.path = True
            current = current.parent