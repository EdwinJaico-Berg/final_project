import pygame
import sys
import time
import math

from pathfinder import Node, Grid

def main():

    algorithms = [
        "a*",
        "djikstra",
        "bfs",
        "dfs",
        "breadth first search",
        "depth first search"
    ]

    # Check usage
    if len(sys.argv) == 2:

        # Parse the command line arguments:
        algorithm = sys.argv[1]
        if algorithm.lower() not in algorithms:
            sys.exit("This algorithm has not been implemented yet")
    
    else:

        # Use a* as default algorithm but print usage
        algorithm = "A*"
        print("===========================================")
        print("Suggested Usage: python runner.py algorithm")
        print("===========================================")

    # Initialise variables
    HEIGHT = 25
    WIDTH = 40
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Create game
    pygame.init()
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

    # Set initial boundaries
    instructions = True
    start = True
    end = True
    barriers = True
    search = True
    found = False

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
            title_rect.center = ((width / 2), 50)
            screen.blit(title, title_rect)

            # Description
            description = [
                "You get to choose the start and end point of the pathfinder",
                f"Using the {algorithm} pathfinding algorithm,", 
                "the shortest path will be calculated"
            ]
            for i, sentence in enumerate(description):
                line = small_font.render(sentence, True, WHITE)
                line_rect = line.get_rect()
                line_rect.center = ((width / 2), 175 + 30 * i)
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
            for row in cells:
                for node in row:

                    # No need to check for obstructions / end point
                    # as these will only be added later
                    i = node.i
                    j = node.j
                    node.draw(i, j, board_origin, cell_size, screen)
            
            # Add start node
            left, _, right = pygame.mouse.get_pressed()

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
            for row in cells:
                for node in row:
                    i = node.i
                    j = node.j
                    node.draw(i, j, board_origin, cell_size, screen)

                    # Add the start node
                    if node.start:
                        screen.blit(pin, node.rect)
            
            # Add end node
            left, _, right = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        node = cells[i][j]
                        if node.rect.collidepoint(mouse):
                            # Marks the node as start
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

            # Check buttons or grid pressed
            left, _, right = pygame.mouse.get_pressed()

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
            
            # Start A* search
            if grid.asearch(board_origin, cell_size, screen, pin, flag):
                search = False
                found = True
            else:
                search = False


        # Once the node has been found
        elif found:
            
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
            """current = grid.end
            while current is not None:
                current.path = True
                current = current.parent"""
            

            # Draw the board
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
                    elif node in grid.open:
                        node.fill(screen, GREEN)
                    elif node in grid.closed:
                        node.fill(screen, RED)

            # Check reset button pressed
            left, _, right = pygame.mouse.get_pressed()

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
                    elif node in grid.open:
                        node.fill(screen, GREEN)
                    elif node in grid.closed:
                        node.fill(screen, RED)

            # Check reset button pressed
            left, _, right = pygame.mouse.get_pressed()

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