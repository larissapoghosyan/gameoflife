import pygame
import numpy as np


class Grid(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        sparse_cells: dict,
        initial_cell_size,
        color_grid,
        color_live,
        color_dead,
    ):
        super().__init__()
        self.screen = screen
        screen_width, screen_height = self.screen.get_size()
        self.initial_cell_size = initial_cell_size
        self.initial_grid_height = screen_height // self.initial_cell_size
        self.initial_grid_width = screen_width // self.initial_cell_size
        self.empt_grid = np.zeros(
            (self.initial_grid_height, self.initial_grid_width), dtype=int
        )

        self.sparse_cells = sparse_cells
        self.cell_size = initial_cell_size
        self.color_grid = color_grid
        self.color_live = color_live
        self.color_dead = color_dead
        # self.empty_grid_updated = empt_grid

        self.zoom_level = 1
        self.camera = pygame.Vector2(0, 0)
        # self.offset = pygame.Vector2(0, 0)

    def update(self, updated_cells=None, zoom_in=None):
        if zoom_in is not None:
            self.zoom(zoom_in)

        self.draw(updated_cells)

    def draw(self, updated_cells=None):
        if updated_cells is not None:
            self.sparse_cells = updated_cells.copy()
        for row in range(1, self.empt_grid.shape[0] - 1):
            for col in range(1, self.empt_grid.shape[1] - 1):
                rect = pygame.Rect(
                    (col * self.cell_size) - self.camera.x,
                    (row * self.cell_size) - self.camera.y,
                    self.cell_size,
                    self.cell_size,
                )
                pos = (row, col)

                if pos in self.sparse_cells:
                    pygame.draw.rect(self.screen, self.color_live, rect)
                else:
                    pygame.draw.rect(self.screen, self.color_dead, rect)

                pygame.draw.rect(self.screen, self.color_grid, rect, 1)

    def zoom(self, zoom_in):
        old_zoom_level = self.zoom_level

        if zoom_in and self.zoom_level < 2:
            self.zoom_level *= 1.05

        elif not zoom_in and self.zoom_level > 0.1:
            self.zoom_level /= 1.05

        self.cell_size = round(self.initial_cell_size * self.zoom_level)

        # self.offset = pygame.Vector2(self.screen.get_size()) / 2
        # self.offset = self.offset * (self.zoom_level / old_zoom_level) - self.offset
        # update camera (sets center for zooming)
        # self.camera = self.camera * (self.zoom_level / old_zoom_level)

        # self.camera.x = self.initial_grid_width * self.zoom_level / 2
        # self.camera.y = self.initial_grid_height * self.zoom_level / 2

        # Offset for camera to keep zoom centered
        # offset = pygame.Vector2(self.screen.get_size()) / 2
        # offset = offset * (self.zoom_level / old_zoom_level) - offset

        # # Offset for camera to keep zoom centered
        # # Calculating the center of the screen in world coordinates
        # center_x = (self.camera.x + self.offset.x + self.screen.get_width() // 2) / old_zoom_level
        # center_y = (self.camera.y + self.offset.y + self.screen.get_height() // 2) / old_zoom_level
        
        # # Calculating the camera position for new zoom level
        # self.camera.x = center_x * self.zoom_level - self.screen.get_width() // 2
        # self.camera.y = center_y * self.zoom_level - self.screen.get_height() // 2

        # self.offset = pygame.Vector2(0, 0)  # Reset the offset after zooming
