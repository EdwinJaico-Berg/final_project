import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node():
    """
    Node. These will construct the grid and will be 
    given information so that the heuristics can be calculated
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
        """
        This will draw the rect
        """
        # Draw the cell
        self.rect = pygame.Rect(
            board_origin[0] + j * cell_size,
            board_origin[1] + i * cell_size,
            cell_size, cell_size
        )
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        

    def fill(self, screen: pygame.Surface, colour: tuple) -> None:
        pygame.draw.rect(screen, colour, self.rect)


class Grid():
    """
    The grid that the visualiser will traverse.
    Constructed of Node objects
    """

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

    def get_neigbours(self, node: Node) -> list:
        """
        Returns a set of nodes that are 
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
    
    
    def heuristics(self, parent: Node, node: Node) -> None:
        """
        Calculate the g, h, and f values, using Eucliadian distance
        for the g and h values
        """
        node.g = parent.g + 1
        node.h = (self.end.i - node.i) ** 2 + (self.end.j - node.j) ** 2
        node.f = node.g + node.h

    
    
    def asearch(self, board_origin, cell_size, screen, pin, flag) -> bool:
        """
        This will perform the A* Search algorithm.
        Usually the open and closed list need to be initialised
        however, these are initialised in the __init__ method.
        """
        
        # Append the starting node to the open list
        self.open.append(self.start)

        # Find min f value while the list is not empty
        while len(self.open) > 0:
            
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

                # Calculate the heuristic values
                self.heuristics(current, neighbour)

                # Check if neighbour already on the open list
                for open_neighbour in self.open:
                    if neighbour == open_neighbour and neighbour.g > open_neighbour.g:
                        continue
                
                self.open.append(neighbour)            

                # Assign parent
                neighbour.parent = current

            # Draw the board
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
                    elif node in self.open:
                        node.fill(screen, GREEN)
                    elif node in self.closed:
                        node.fill(screen, RED)

            pygame.display.update()

        # If open no longer has nodes
        return False


    def find_path(self) -> None:
        """
        Marks nodes as belonging to the path
        """
        current = self.end

        while current is not None:
            current.path = True
            current = current.parent
