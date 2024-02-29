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

        self.sparse_cells: Dict[Tuple[int, int], int] = {}

        self.screen = screen
        self.viewScale = viewScale
        self.screen_width, self.screen_height = screen.get_size()

        self.camera_x = 0
        self.camera_y = 0

        self.color_grid = color_grid
        self.color_living_cell = color_living_cell

    def update(self, new_sparse_cells):
        self.draw(new_sparse_cells)

    @property
    def scaled_cell_size(self) -> int:
        cell_size = 1
        return cell_size * self.viewScale

    @property
    def mouse_pos(self) -> Tuple[int, int]:
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        self._mouse_pos = pos

    def adjust_view_scale(self, delta: int):
        original_view_scale = self.viewScale
        self.viewScale += delta
        self.viewScale = min(500, self.viewScale)
        self.viewScale = max(3, self.viewScale)

        mouse_x, mouse_y = self._mouse_pos

        # Calculate original world position of the mouse
        pre_zoom_x = (mouse_x + self.camera_x) / original_view_scale
        pre_zoom_y = (mouse_y + self.camera_y) / original_view_scale

        # After zoom, calculate the new position of the mouse in game world
        post_zoom_x = (mouse_x + self.camera_x) / self.viewScale
        post_zoom_y = (mouse_y + self.camera_y) / self.viewScale

        world_shift_x = post_zoom_x - pre_zoom_x
        world_shift_y = post_zoom_y - pre_zoom_y

        x = round(world_shift_x * original_view_scale + 1)
        y = round(world_shift_y * original_view_scale + 1)
        self.adjust_camera_view(dx=x, dy=y)
        # self.camera_x = x
        # self.camera_y = y

    def adjust_camera_view(self, dx: int, dy: int):
        self.camera_x += dx
        self.camera_y += dy

    def calc_grid_dimensions(self) -> Tuple[int, int, int, int]:
        start_pos_y = - self.camera_y // self.scaled_cell_size
        start_pos_x = - self.camera_x // self.scaled_cell_size
        return (
            start_pos_y,
            start_pos_y + (self.screen_height // self.scaled_cell_size) + 1,  # end_pos_y
            start_pos_x,
            start_pos_x + (self.screen_width // self.scaled_cell_size) + 1,  # end_pos_x
        )

    def draw(self, new_sparse_cells):
        if new_sparse_cells:
            self.sparse_cells = new_sparse_cells

        start_pos_y, end_pos_y, start_pos_x, end_pos_x = self.calc_grid_dimensions()

        for row in range(start_pos_y, end_pos_y):
            for col in range(start_pos_x, end_pos_x):
                # Rect(left(x_cord), top(y_cord), cell_width, cell_height)
                rect = pygame.Rect(
                    col * self.scaled_cell_size + self.camera_x,
                    row * self.scaled_cell_size + self.camera_y,
                    self.scaled_cell_size,
                    self.scaled_cell_size
                )

                if new_sparse_cells.get((row, col)):
                    pygame.draw.rect(self.screen, self.color_living_cell, rect)
                pygame.draw.rect(self.screen, self.color_grid, rect, width=1)

        # for row in range(start_pos_y, end_pos_y):
        #     min_x = +100000000
        #     max_x = -100000000
        #     min_y = +100000000
        #     max_y = -100000000
        #     for col in range(start_pos_x, end_pos_x):
        #         start_x = col * self.scaled_cell_size + self.camera_x
        #         start_y = row * self.scaled_cell_size + self.camera_y
        #         size_x = self.scaled_cell_size
        #         size_y = self.scaled_cell_size
        #         min_x = min(min_x, start_x)
        #         min_y = min(min_y, start_y)
        #         max_x = max(max_x, start_x + size_x)
        #         max_y = max(max_y, start_y + size_y)
        #     rect = pygame.Rect(
        #         min_x,
        #         min_y,
        #         max_x - min_x,
        #         max_y - min_y
        #     )

        #     pygame.draw.rect(self.screen, self.color_grid, rect, width=1)
