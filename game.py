import sys
import pygame
import numpy as np
from cells import Cells
from grid import Grid
from game_controls import GameControls
import events


def run():
    pygame.init()
    # Determine screen dimensions
    screenWidth = 1200
    screenHeight = 800
    # extra_space = 220

    #  game colors
    background_color = (255, 189, 216)
    color_living_cell = (255, 81, 72)
    color_grid = (255, 220, 225)

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Conway's game of Life")

    clock = pygame.time.Clock()

    # Grid dimensions
    CELLSIZE = 15
    GRID_WIDTH = (screenWidth) // CELLSIZE
    GRID_HEIGHT = screenHeight // CELLSIZE

    # Create the grid
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

    cells = Cells(screenWidth, grid, CELLSIZE)

    draw_grid = Grid(
        screen,
        cells.sparse_cells,
        CELLSIZE,
        color_grid=color_grid,
        color_live=color_living_cell,
        color_dead=background_color,
    )

    game_controls = GameControls(
        screen, screenWidth, screenHeight, grid, draw_grid, CELLSIZE
    )

    pygame.time.set_timer(events.STEP_EVENT, 150)

    # Main game loop
    running = True
    while running:
        # update screen at 60 (or 120) FPS
        clock.tick(120)

        # Fill screen with background_color
        screen.fill(background_color)

        # process all events
        for event in pygame.event.get():
            # print(event.type)
            # mouse_pos = pygame.mouse.get_pos()
            # print(f"Mouse Position: {mouse_pos}")
            cells.handle_event(event)
            # game_controls.slider.handle_event(event, )
            # sliderButton.handle_event(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL]:
                continue

            action = game_controls.process_mouse_input(event, cells.sparse_cells)

            if action is None:
                continue

            action_key, grid_pos = action

            if action_key == "add_cell":
                cells.add_cell(grid_pos)

            elif action_key == "remove_cell":
                cells.remove_cell(grid_pos)

            elif action_key == "is_playing":
                cells.is_playing = game_controls.is_playing

            elif action_key == "reset":
                cells.reset()

            elif action_key == "clear":
                cells.clear()

            elif action_key == "save":
                cells.save("saved_state/saved_state.json")

            elif action_key == "load":
                cells.load("saved_state/saved_state.json")

        # -Update the current grid with the new one
        draw_grid.update(updated_cells=cells.sparse_cells)

        # Draw the buttons (play, pause, reset, clear, save, slider)
        # game_controls.draw_container()
        game_controls.draw_buttons()

        # -Update display
        pygame.display.flip()

    # Quit the game
    pygame.quit()
    sys.exit()
