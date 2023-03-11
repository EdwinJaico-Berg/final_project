import pygame

# Initialise variables
HEIGHT = 25
WIDTH = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# algorithms
algorithms = {
    "asearch": "A* search",
    "astar": "A* search",
    "djikstra": "Djikstra's",
    "bfs": "Breadth First Search",
    "dfs": "Depth First Search",
    "breadth first search": "Breadth First Search",
    "depth first search": "Depth First Search",
    "greedy": "Greedy",
}

# Compute board size
BOARD_PADDING = 20
size = width, height = 600, 500
board_width = width - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING + 100)
