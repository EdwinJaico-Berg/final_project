import pygame
import sys
import time
import numpy as np

from pathfinder import Node, Grid

def main():

    # Initialise algorithm variables
    algorithm = None
    algorithms = {
        "asearch": "A* search",
        "a*": "A* search",
        "djikstra": "Djikstra's",
        "bfs": "Breadth First Search",
        "dfs": "Depth First Search",
        "breadth first search": "Breadth First Search",
        "depth first search": "Depth First Search",
        "greedy": "Greedy"
    }

    # Check usage
    if len(sys.argv) in [2, 3]:

        # Parse the command line arguments:
        algorithm = sys.argv[1]
        if algorithm.lower() not in algorithms:
            sys.exit("This algorithm has not been implemented yet")
    
    else:

        # Use a* as default algorithm but print usage
        algorithm = "A*"
        print("------------------------------------------------")
        print("Suggested Usage: python runner.py algorithm maze")
        print("------------------------------------------------")

    # Initialise variables
    HEIGHT = 25
    WIDTH = 40
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Create game
    pygame.init()
    pygame.display.set_caption('Pathfinder')
    icon = pygame.image.load("assets/images/icon.png")
    pygame.display.set_icon(icon)
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)

    # Fonts
    WALKWAY = "assets/fonts/Walkway_UltraBold.ttf"
    small_font = pygame.font.Font(WALKWAY, 20)
    medium_font = pygame.font.Font(WALKWAY, 28)
    large_font = pygame.font.Font(WALKWAY, 40)
    
    # Compute board size
    BOARD_PADDING = 20
    board_width = width - (BOARD_PADDING  * 2)
    board_height = height - (BOARD_PADDING * 2)
    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
    board_origin = (BOARD_PADDING, BOARD_PADDING + 100)

    # Add the flag (end) and pin (start) image
    pin = pygame.image.load("assets/images/pin.jpeg")
    pin = pygame.transform.scale(pin, (cell_size - 2, cell_size - 2))
    flag = pygame.image.load("assets/images/flag.png")
    flag = pygame.transform.scale(flag, (cell_size - 2, cell_size - 2))

    # Initialise the grid
    grid = Grid(HEIGHT, WIDTH)
    cells = grid.cells

    mask = None

    # Generate maze if asked
    try:
        if sys.argv[2]:
            mask = np.random.randint(0, 2, (HEIGHT,WIDTH))
            grid.generate_maze(mask)
    except IndexError:
        pass

    # Set logical barriers
    instructions = True
    start = True
    end = True
    barriers = True
    search = True
    found = False
    path = False

    # Create draw board function
    def draw_board(cells, board_origin, cell_size, screen, grid) -> None:
        '''Draw the rects for the nodes.'''
        
        for row in cells:
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
                elif node.path:
                    node.fill(screen, BLUE)
                elif node in grid.closed:
                    node.fill(screen, RED)
                elif node in grid.open:
                    node.fill(screen, GREEN)

    while True:

        # Check if game is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.fill(BLACK)

        # Show visualiser instructions
        if instructions:

            # Title
            title = large_font.render("Pathfinding Visualiser", True, WHITE)
            title_rect = title.get_rect()
            title_rect.center = ((width / 2), 100)
            screen.blit(title, title_rect)

            # Description
            description = [
                "You get to choose the start and end point of the pathfinder",
                f"Using the {algorithms[sys.argv[1]]} pathfinding algorithm,", 
                "the shortest path will be calculated"
            ]
            for i, sentence in enumerate(description):
                line = small_font.render(sentence, True, WHITE)
                line_rect = line.get_rect()
                line_rect.center = ((width / 2), 215 + 30 * i)
                screen.blit(line, line_rect)

            # Start button
            button_rect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
            button_text = medium_font.render("Start", True, BLACK)
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            pygame.draw.rect(screen, WHITE, button_rect)
            screen.blit(button_text, button_text_rect)
            
            # Check button input
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    instructions = False
                    time.sleep(0.3)
        
        # Show instructions to place start node
        elif start:
            
            # Write instructions on screen
            instruction = medium_font.render("Place start node", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 2), 50)
            screen.blit(instruction, instruction_rect)

            # Draw the board
            draw_board(cells, board_origin, cell_size, screen, grid)
            
            # Add start node
            left, _, _ = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        node = cells[i][j]
                        if node.rect.collidepoint(mouse):
                            # Marks the node as start
                            node.start = True
                            grid.start = node
                            start = False
                            time.sleep(0.3)
        
        # Show instructions to place end node
        elif end:
            
            # Write instructions
            instruction = medium_font.render("Place end node", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 2), 50)
            screen.blit(instruction, instruction_rect)

            # Draw the board
            draw_board(cells, board_origin, cell_size, screen, grid)
            
            # Add end node
            left, _, _ = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        node = cells[i][j]
                        if node.rect.collidepoint(mouse):
                            # Marks the node as start
                            if not node.start:
                                node.end = True
                                grid.end = node
                                end = False
                                time.sleep(0.3)
        
        # Show instructions to draw barriers
        elif barriers:
            
            # Write instructions
            instruction = medium_font.render("Draw barriers", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 3), 50)
            screen.blit(instruction, instruction_rect)

            # Search button
            search_button = pygame.Rect(
                (width * (1 / 2)) + BOARD_PADDING, 30, 
                100, 40
            )
            search_button_text = medium_font.render("Search", True, BLACK)
            search_button_rect = search_button_text.get_rect()
            search_button_rect.center = search_button.center
            pygame.draw.rect(screen, WHITE, search_button)
            screen.blit(search_button_text, search_button_rect)

            # Reset button
            reset_button = pygame.Rect(
                (width * (1 / 2)) + BOARD_PADDING + 115, 30,
                100, 40 
            )
            reset_button_text = medium_font.render("Reset", True, BLACK)
            reset_button_rect = reset_button_text.get_rect()
            reset_button_rect.center = reset_button.center
            pygame.draw.rect(screen, WHITE, reset_button)
            screen.blit(reset_button_text, reset_button_rect)
            

            # Draw the board
            draw_board(cells, board_origin, cell_size, screen, grid)

            # Check buttons or grid pressed
            left, _, _ = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()
                
                # If search button is clicked, start the search
                if search_button.collidepoint(mouse):
                    barriers = False
                    time.sleep(0.3)
                    
                elif reset_button.collidepoint(mouse):

                    # Re-initialise all the variables
                    grid = Grid(HEIGHT, WIDTH)
                    cells = grid.cells
                    start = True
                    end = True
                    barriers = True
                else:
                    for i in range(HEIGHT):
                        for j in range(WIDTH):
                            node = cells[i][j]
                            if node.rect.collidepoint(mouse):
                                if node.start or node.end:
                                    continue
                                else:
                                    # Marks the node as an obstruction
                                    node.obstruction = True
        
        # Show search
        elif search:
            
            # Write instructions
            instruction = medium_font.render("Searching...", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 2), 50)
            screen.blit(instruction, instruction_rect)

            algos = {'A* search': grid.asearch, "Djikstra's": grid.djikstra, 
                     'Greedy': grid.greedy, 'Breadth First Search': grid.bfs, 
                     'Depth First Search': grid.dfs}
            
            # Start algorithm search depending on input
            algo = algorithms[algorithm.lower()]

            if algos[algo](board_origin, cell_size, screen, pin, flag):
                found = True
                path = True
                search = False
            else:
                search = False


        # Once the node has been found
        elif found and grid.open:
            
            # Write instructions
            instruction = medium_font.render("Path Found!", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 3), 50)
            screen.blit(instruction, instruction_rect)

            # Reset button
            reset_button = pygame.Rect(
                (width * (1 / 2)) + BOARD_PADDING + 30, 30,
                100, 40 
            )
            reset_button_text = medium_font.render("Reset", True, BLACK)
            reset_button_rect = reset_button_text.get_rect()
            reset_button_rect.center = reset_button.center
            pygame.draw.rect(screen, WHITE, reset_button)
            screen.blit(reset_button_text, reset_button_rect)
            
            # Draw the path
            grid.find_path()

            # Draw the board
            draw_board(cells, board_origin, cell_size, screen, grid)

            # Check reset button pressed
            left, _, _ = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()

                if reset_button.collidepoint(mouse):

                    # Re-initialise all the variables
                    grid = Grid(HEIGHT, WIDTH)
                    grid.generate_maze(mask)
                    cells = grid.cells
                    start = True
                    end = True
                    barriers = True
                    search = True

        else:
            # Write instructions
            instruction = medium_font.render("No path found...", True, WHITE)
            instruction_rect = instruction.get_rect()
            instruction_rect.center = ((width / 3), 50)
            screen.blit(instruction, instruction_rect)

            # Reset button
            reset_button = pygame.Rect(
                (width * (1 / 2)) + BOARD_PADDING + 30, 30,
                100, 40 
            )
            reset_button_text = medium_font.render("Reset", True, BLACK)
            reset_button_rect = reset_button_text.get_rect()
            reset_button_rect.center = reset_button.center
            pygame.draw.rect(screen, WHITE, reset_button)
            screen.blit(reset_button_text, reset_button_rect)

            # Draw the board
            draw_board(cells, board_origin, cell_size, screen, grid)

            # Check reset button pressed
            left, _, _ = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()

                if reset_button.collidepoint(mouse):

                    # Re-initialise all the variables
                    grid = Grid(HEIGHT, WIDTH)
                    cells = grid.cells
                    start = True
                    end = True
                    barriers = True
                    search = True


        pygame.display.flip()

if __name__ == "__main__": 
    main()