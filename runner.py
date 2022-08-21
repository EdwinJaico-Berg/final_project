from email.header import Header
import pygame
import sys
import time

from pathfinder import Node, Grid, PathFindingAI

def main():
    
    # Initialise variables
    HEIGHT = 25
    WIDTH = 40
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    WHITE = (255, 255, 255)

    # Create game
    pygame.init()
    size = width, height = 600, 400
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
    board_origin = (BOARD_PADDING, BOARD_PADDING)

    # Add the flag (end) and pin (start) image
    pin = pygame.image.load("assets/images/pin.jpeg")
    pin = pygame.transform.scale(pin, (cell_size, cell_size))
    flag = pygame.image.load("assets/images/flag.png")
    flag = pygame.transform.scale(flag, (cell_size, cell_size))

    # Initialise the grid
    grid = Grid(HEIGHT, WIDTH)
    cells = grid.cells

    # Show instructions initially
    instructions = True

    while True:

        # Check if game is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.fill(WHITE)

        # Show visualiser instructions
        if instructions:

            # Title
            title = large_font.render("Pathfinding Visualiser", True, BLACK)
            title_rect = title.get_rect()
            title_rect.center = ((width / 2), 50)
            screen.blit(title, title_rect)

            # Description
            description = [
                "You get to choose the start and end point of the pathfinder",
                "Using the A* pathfinding algorithm,", 
                "the shortest path will be calculated"
            ]
            for i, sentence in enumerate(description):
                line = small_font.render(sentence, True, BLACK)
                line_rect = line.get_rect()
                line_rect.center = ((width / 2), 150 + 30 * i)
                screen.blit(line, line_rect)

            # Start button
            button_rect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
            button_text = medium_font.render("Start", True, WHITE)
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            pygame.draw.rect(screen, BLACK, button_rect)
            screen.blit(button_text, button_text_rect)
            
            # Check button input
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse):
                    instructions = False
                    time.sleep(0.3)

            pygame.display.flip()
            continue

        # Draw the board
        for row in cells:
            for node in row:
                i = node.i
                j = node.j
                node.draw(i, j, board_origin, cell_size, screen)

                if node.obstruction:
                    pygame.draw.rect(screen, BLACK, node.rect)
                if node.start:
                    screen.blit(pin, node.rect)
                if node.end:
                    screen.blit(flag, node.rect)

        # Add blocked cells
        left, _, right = pygame.mouse.get_pressed()

        if left == 1:
                
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    node = cells[i][j]
                    if node.rect.collidepoint(mouse):
                        # Marks the node as an obstruction
                        node.obstruction = True
                    
        pygame.display.flip()




if __name__ == "__main__":
    main()