import pygame
import events
import json


class Cells(pygame.sprite.Sprite):
    def __init__(self, screen_width, grid, size):
        super().__init__()
        self.screen_width = screen_width
        self.grid = grid
        self.cell_size = size

        self.sparse_cells = {}
        self.initial_input = {}

        self.is_playing = False

    def handle_event(self, event):
        if event.type == events.STEP_EVENT:
            self.update()

    @classmethod
    def num_living_neighbors(cls, coordinates, point):
        row, col = point
        neighbors = [
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        ]
        return sum(coordinates.get(p, 0) for p in neighbors)

    def update(self):
        if self.is_playing:
            self.change_state()

    def change_state(self):
        updated_cells = {}

        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                pos = (row, col)
                s = self.num_living_neighbors(self.sparse_cells, pos)

                if pos in self.sparse_cells and (2 <= s <= 3):
                    updated_cells[pos] = 1
                elif pos not in self.sparse_cells and s == 3:
                    updated_cells[pos] = 1

        self.sparse_cells = updated_cells

    def add_cell(self, pos):
        self.sparse_cells[pos] = 1
        self.initial_input = self.sparse_cells.copy()

    def remove_cell(self, pos):
        del self.sparse_cells[pos]

    def reset(self):
        self.sparse_cells = self.initial_input.copy()

    def clear(self):
        self.sparse_cells = {}

    def save(self, filename):
        save_state = [k for k, _ in self.sparse_cells.items()]
        with open(filename, "w") as f:
            json.dump(save_state, f)

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                loaded_list = json.load(f)

            # LEGACY COMPATIBILITY LAYER
            if isinstance(loaded_list, dict):
                print(
                    "warning: loading from the old format, please upgrade to our more efficient format"
                )
                loaded_list = [eval(k) for k, _ in loaded_list.items()]

            loaded_dict = {tuple(k): 1 for k in loaded_list}

            self.sparse_cells = loaded_dict
            self.initial_input = self.sparse_cells.copy()

        except FileNotFoundError:
            print("FileNotFoundError: No such file or directory")
