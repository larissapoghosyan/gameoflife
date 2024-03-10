import pygame
import events
import json
from grid import Grid
from typing import List, Tuple, Dict


class Cells(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        grid: 'Grid'
    ):
        super().__init__()
        self.screen = screen
        self.sparse_cells: Dict[Tuple[int, int], int] = {}
        self.initial_input: Dict[Tuple[int, int], int] = {}

        self.is_playing = False
        self.next_state = None

        self.grid = grid

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
        self.sparse_cells[pos] = 1
        self.initial_input = self.sparse_cells.copy()

    def remove_cell(self, pos: Tuple[int, int]):
        del self.sparse_cells[pos]

    def reset(self):
        self.sparse_cells = self.initial_input.copy()

    def clear(self):
        self.sparse_cells = {}

    def next(self):
        self.is_playing = False
        self.step()

    def save(self, filename: str):
        save_state = [k for k, _ in self.sparse_cells.items()]
        with open(filename, "w") as f:
            save_dict = {
                'saved_state': save_state,
                'camera_pos': (self.grid.camera_x, self.grid.camera_y),
                'viewScale': self.grid.viewScale,
                'version': 1.0
            }
            json.dump(save_dict, f)

    def load(self, filename: str):
        try:
            with open(filename, "r") as f:
                loaded_data = json.load(f)

            # LEGACY COMPATIBILITY LAYER
            if isinstance(loaded_data, dict):
                try:
                    version = loaded_data.get("version", 0)
                    if version == 1.0:
                        # handle data with version 1.0
                        loaded_list = loaded_data['saved_state']
                        self.grid.camera_x, self.grid.camera_y = loaded_data['camera_pos']
                        self.grid.viewScale = loaded_data['viewScale']
                    elif version == 0:
                        # handle data with no version number (version 0)
                        print("Warning: loading from the old format, please upgrade to the more efficient format")
                        loaded_list = [eval(k) for k, _ in loaded_data.items()]
                except KeyError:
                    print("Error: Missing required keys in loaded data")
                    return
            elif isinstance(loaded_data, list):
                # handle list input
                loaded_list = loaded_data
            else:
                print("Error: unrecognized data format")
                return

            loaded_dict: Dict[Tuple[int, int], int] = {tuple(k): 1 for k in loaded_list}

            self.sparse_cells = loaded_dict
            self.initial_input = self.sparse_cells.copy()

        except FileNotFoundError:
            print("FileNotFoundError: No such file or directory")
