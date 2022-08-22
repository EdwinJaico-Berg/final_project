import pygame
import math

BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

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
        node.g = parent.g + math.sqrt((parent.i - node.i) ** 2 + (parent.j - node.j) ** 2)
        node.h = math.sqrt((self.end.i - node.i) ** 2 + (self.end.j - node.j) ** 2)
        node.f = node.g + node.h

    
    
    def asearch(self) -> bool:
        """
        This will perform the A* Search algorithm.
        Usually the open and closed list need to be initialised
        however, these are initialised in the __init__ method.
        """
        
        # Append the starting node to the open list
        self.open.append(self.start)

        # Find min f value while the list is not empty
        while len(self.open) > 0:
            current = None
            min_f = math.inf
            for index, node in enumerate(self.open):
                if node.f < min_f:
                    min_f = node.f
                    current = node
                    current_index = index
            
            # Pop q off the list
            self.open.pop(current_index)
            self.closed.append(current)

            # Check current node is the goal
            if current == self.end:
                return True

            # Generate the neighbours
            neighbours = self.get_neigbours(current)
            
            for neighbour in neighbours:

                # Set a parent
                neighbour.parent = current
                
                # Check whether neighbour has been searched
                for closed_neighbour in self.closed:
                    if neighbour == closed_neighbour:
                        continue

                # Calculate the heuristic values
                self.heuristics(neighbour.parent, neighbour)

                # Check if neighbour already on the open list
                for open_neighbour in self.open:
                    if neighbour == open_neighbour and neighbour.g > open_neighbour.g:
                        continue

                self.open.append(neighbour)