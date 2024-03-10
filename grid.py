import pygame
from typing import Tuple, Dict


class Grid(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        color_grid: Tuple[int, int, int],
        color_living_cell: Tuple[int, int, int],
        viewScale: int,
    ):
        super().__init__()
        self._mouse_pos: Tuple[int, int] = None

        self.screen = screen
        self.viewScale = viewScale
        self.screen_width, self.screen_height = screen.get_size()

        self.camera_x = 0
        self.camera_y = 0

        self.color_grid = color_grid
        self.color_living_cell = color_living_cell

    def update(self, updated_sparse_cells):
        self.draw(updated_sparse_cells)

    @property
    def adjusted_cell_size(self) -> int:
        cell_size = 1
        return cell_size * self.viewScale

    @property
    def mouse_pos(self) -> Tuple[int, int]:
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        self._mouse_pos = pos

    def adjust_view_scale(self, delta: int):
        mouse_x, mouse_y = self.mouse_pos
        initial_camera_x = self.camera_x
        initial_camera_y = self.camera_y
        initial_viewscale = self.viewScale

        self.viewScale += delta
        self.viewScale = min(500, self.viewScale)
        self.viewScale = max(3, self.viewScale)

        # adjust camera position, to zoom in our out on the current mouse position
        self.camera_x = mouse_x - (mouse_x - initial_camera_x) * (self.viewScale / initial_viewscale)
        self.camera_y = mouse_y - (mouse_y - initial_camera_y) * (self.viewScale / initial_viewscale)

    def adjust_camera_view(self, dx: int, dy: int):
        self.camera_x += dx
        self.camera_y += dy

    def calc_grid_dimensions(self) -> Tuple[int, int, int, int]:
        start_pos_j: int = - self.camera_y // self.adjusted_cell_size
        start_pos_i: int = - self.camera_x // self.adjusted_cell_size
        return (
            int(start_pos_j),
            int(start_pos_j + (self.screen_height // self.adjusted_cell_size) + 2),  # end_pos_y
            int(start_pos_i),
            int(start_pos_i + (self.screen_width // self.adjusted_cell_size) + 2),  # end_pos_x
        )

    def draw(self, updated_sparse_cells):
        start_pos_j, end_pos_j, start_pos_i, end_pos_i = self.calc_grid_dimensions()

        for row in range(start_pos_j, end_pos_j):
            for col in range(start_pos_i, end_pos_i):
                # Rect(left(x_cord), top(y_cord), cell_width, cell_height)
                rect = pygame.Rect(
                    col * self.adjusted_cell_size + self.camera_x,
                    row * self.adjusted_cell_size + self.camera_y,
                    self.adjusted_cell_size,
                    self.adjusted_cell_size
                )

                if updated_sparse_cells.get((row, col)):
                    pygame.draw.rect(self.screen, self.color_living_cell, rect)
                pygame.draw.rect(self.screen, self.color_grid, rect, width=1)

        # for row in range(start_pos_y, end_pos_y):
        #     min_x = +100000000
        #     max_x = -100000000
        #     min_y = +100000000
        #     max_y = -100000000

        #     rect = pygame.Rect(
        #         min_x,
        #         min_y,
        #         max_x - min_x,
        #         max_y - min_y
        #     )
        #     pygame.draw.rect(self.screen, self.color_grid, rect, width=1)

        #     for col in range(start_pos_x, end_pos_x):
        #         start_x = col * self.adjusted_cell_size + self.camera_x
        #         start_y = row * self.adjusted_cell_size + self.camera_y
        #         size_x = self.adjusted_cell_size
        #         size_y = self.adjusted_cell_size
        #         min_x = min(min_x, start_x)
        #         min_y = min(min_y, start_y)
        #         max_x = max(max_x, start_x + size_x)
        #         max_y = max(max_y, start_y + size_y)

        #         rect = pygame.Rect(
        #             min_x,
        #             min_y,
        #             max_x - min_x,
        #             max_y - min_y
        #         ) 
        #         pygame.draw.rect(self.screen, self.color_grid, rect, width=1)
