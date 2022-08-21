import pygame

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
        self.f = 0
        self.g =  0
        self.h = 0

        # Show whether the node is an obstruction or not
        self.obstruction = False

        # Variable for the neighbours of the node
        self.neighbours = set()
    
    
    def __eq__(self, __o: object) -> bool:
        return (
            (self.i == __o.i) and
            (self.j == __o.j)
        )

    
    def draw(self, i: int, j: int, board_origin: int, cell_size: int, screen) -> None:
        """
        This will draw the rect
        """
        # Draw the cell
        rect = pygame.Rect(
            board_origin[0] + j * cell_size,
            board_origin[1] + i * cell_size,
            cell_size, cell_size
        )
        pygame.draw.rect(screen, BLACK, rect, 1)

    def fill(self):
        raise NotImplementedError



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

    def get_neigbours(self, node: Node) -> set:
        """
        Returns a set of nodes that are 
        """
        neighbours = set()

        for i in range(node.i - 1, node.i + 2):
            for j in range(node.j - 1, node.j + 2):
                
                # Check it falls within the grid
                if 0 <= i < self.height and 0 <= j < self.width:
                    
                    # Define a Node variable called neighbour
                    neighbour = self.cells[i][j]
                    
                    # Ignore the cell itself
                    if node != neighbour and not node.obstruction:
                        neighbours.add(neighbour)

        return neighbours




class PathFindingAI():
    """
    Pathfinding agent
    """

    def __init__(self, height: int=25, width: int=25):
        
        # Set initial height and width
        self.height = height
        self.width = width
