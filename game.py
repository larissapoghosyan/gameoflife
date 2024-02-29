import sys
import pygame
from cells import Cells
from grid import Grid
from game_controls import GameControls
import events


def run():
    pygame.init()

    screen_width = 1200
    screen_height = 700

    # game colors
    background_color = (130, 228, 228)
    color_living_cell = (245, 110, 202)
    color_grid = (204, 244, 244)

    pygame.display.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Conway's GameofLife")

    clock = pygame.time.Clock()
    pygame.time.set_timer(events.STEP_EVENT, 150)

    viewScale = 20

    cells = Cells(screen)

    grid = Grid(
        screen=screen,
        color_grid=color_grid,
        color_living_cell=color_living_cell,
        viewScale=viewScale,
    )

    controls = GameControls(screen)

    running = True
    while running:
        # update at every 120 FPS
        clock.tick(120)

        # fill screen surface with background color
        screen.fill(background_color)

        # process all events
        for event in pygame.event.get():
            cells.handle_event(event)

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type not in [
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION,
                pygame.MOUSEWHEEL
            ]:
                continue

            action = controls.process_mouse_input(
                event,
                sparse_cells=cells.sparse_cells,
                grid=grid
            )

            if action is None:
                continue

            action_key, value = action

            if action_key == "is_playing":
                cells.is_playing = controls.is_playing

            elif action_key == "panning":
                dx, dy = value
                grid.adjust_camera_view(dx=dx, dy=dy)

            elif action_key == "viewpoint":
                grid.adjust_view_scale(event.y)

            elif action_key == "load":
                cells.load("saved_state/gosper_glider_gun.json")

        grid.update(new_sparse_cells=cells.sparse_cells)

        controls.draw_buttons()

        # update display (update and flip are the same,
        # tho update can be used for spot updates too)
        pygame.display.flip()

    # quit the game
    pygame.quit()
    sys.exit()
