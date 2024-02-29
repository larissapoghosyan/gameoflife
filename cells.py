import pygame
import events
import json
from grid import Grid
from typing import List, Tuple, Dict


class Cells(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        # update_cells_event: events.Event
    ):
        super().__init__()
        # self.update_cells_event = update_cells_event
        self.screen = screen
        self.sparse_cells: Dict[Tuple[int, int], int] = {}
        self.initial_input: Dict[Tuple[int, int], int] = {}

        self.is_playing = False

        # self.sparse_cells[(0, 0)] = 1
        # self.sparse_cells[(1, 0)] = 1
        # self.sparse_cells[(0, 1)] = 1
        # self.sparse_cells[(2, 0)] = 1
        # self.sparse_cells[(0, 2)] = 1
        self.sparse_cells[(0, 1)] = 1
        self.sparse_cells[(1, 2)] = 1
        self.sparse_cells[(2, 2)] = 1
        self.sparse_cells[(2, 1)] = 1
        self.sparse_cells[(2, 0)] = 1

        # self.sparse_cells[(1, 0)] = 1
        # self.sparse_cells[(1, 2)] = 1
        # self.sparse_cells[(2, 1)] = 1
        # self.sparse_cells[(2, 2)] = 1
        # self.sparse_cells[(3, 1)] = 1

        # (1, 0), (1, 2), (2, 1), (2, 2), , (3, 1)

    def handle_event(self, event):
        if event.type == events.STEP_EVENT:
            self.update()

    def get_all_neightbors(
            self,
            cell: Tuple[int, int]
    ) -> Dict[Tuple[int, int], int]:

        (y, x) = cell
        delta = [-1, 0, 1]

        neighbors = {}
        for dy in delta:
            for dx in delta:
                if dy == 0 and dx == 0:
                    continue
                neighbor_cell = (y + dy, x + dx)
                neighbors[neighbor_cell] = 1 if neighbor_cell in self.sparse_cells else 0

        return neighbors

    def update(self):
        # passes sparse_cells to event triggerer for event
        # listener grid to get updated sparse cells at every iteration
        # self.update_cells_event.trigger_event(self.sparse_cells)
        if self.is_playing:
            self.step()

    def step(self):
        updated_sparse_cells = {}
        candidates = self.sparse_cells.copy()

        for cell in self.sparse_cells:
            candidates.update(self.get_all_neightbors(cell))

        for cell in candidates:
            all_neighbors = list(self.get_all_neightbors(cell).values())
            num_live_neighbors = sum(all_neighbors)

            if num_live_neighbors == 3 or (
                num_live_neighbors == 2
                and cell in self.sparse_cells
            ):
                updated_sparse_cells[cell] = 1

        self.sparse_cells = updated_sparse_cells

    def add_cell(self, pos: Tuple[int, int]):
        pass

    def remove_cell(self, pos: Tuple[int, int]):
        pass

    def reset(self):
        pass

    def clear(self):
        pass

    def save(self, filename: str):
        pass

    def load(self, filename: str):
        try:
            with open(filename, "r") as f:
                loaded_list: List[Tuple[int, int]] = json.load(f)

            # LEGACY COMPATIBILITY LAYER
            if isinstance(loaded_list, dict):
                print(
                    "warning: loading from the old format, please upgrade to our more efficient format"
                )
                loaded_list = [eval(k) for k, _ in loaded_list.items()]

            loaded_dict: Dict[Tuple[int, int], int] = {tuple(k): 1 for k in loaded_list}

            self.sparse_cells = loaded_dict
            self.initial_input = self.sparse_cells.copy()

        except FileNotFoundError:
            print("FileNotFoundError: No such file or directory")
