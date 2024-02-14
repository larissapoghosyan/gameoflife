import pygame
from grid import Grid


class GameControls(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        screen_width,
        screen_height,
        grid,
        grid_obj,
        cell_size,
    ):
        super().__init__()
        self.count = 0
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid = grid
        self.grid_obj = grid_obj
        self.cell_size = cell_size

        self.buffer_space = 10
        self.container_width = self.screen_width // 7 - 2 * self.buffer_space
        self.container_height = self.screen_width // 4 - 2 * self.buffer_space
        self.container_surface_rect = None

        self.is_playing = False
        self.play_button, self.play_button_rect = self.create_button(
            "icons", "play.png", x_pos=self.container_width - 40, y_pos=20
        )
        self.pause_button, self.pause_button_rect = self.create_button(
            "icons", "pause.png", x_pos=self.container_width - 40, y_pos=20
        )
        self.reset_button, self.reset_button_rect = self.create_button(
            "icons", "reset.png", x_pos=self.container_width - 40, y_pos=70
        )
        self.clear_button, self.clear_button_rect = self.create_button(
            "icons", "clear.png", x_pos=self.container_width - 40, y_pos=120
        )
        self.save_button, self.save_button_rect = self.create_button(
            "icons", "save.png", x_pos=self.container_width - 40, y_pos=170
        )
        self.upload_button, self.upload_button_rect = self.create_button(
            "icons", "upload.png", x_pos=self.container_width - 40, y_pos=220
        )
        self.zoom_in_button, self.zoom_in_button_rect = self.create_button(
            "icons", "plus.png", x_pos=self.container_width - 60, y_pos=270
        )
        self.zoom_out_button, self.zoom_out_button_rect = self.create_button(
            "icons", "minus.png", x_pos=self.container_width - 20, y_pos=270
        )

    @classmethod
    def load_resource_image(cls, dir_name: str, name: str) -> pygame.Surface:
        import os

        resource_dir = os.path.dirname(__file__)
        path = os.path.join(resource_dir, dir_name, name)
        return pygame.image.load(path)

    @classmethod
    def create_button(cls, dir_name, image_name, x_pos, y_pos):
        img_dimension = (30, 30)
        button = cls.load_resource_image(dir_name, image_name)
        button = pygame.transform.scale(button, img_dimension)
        button_rect = button.get_rect()
        button_rect.topright = (x_pos, y_pos)
        return button, button_rect

    def convert_pixel_pos_to_grid(self, mouse_y, mouse_x):
        # convert positional coordinates into grid_cells,
        #  which cell containes the pixel that was clicked:
        # Convert positional coordinates into cells
        grid_y = (mouse_y) // self.grid_obj.cell_size
        grid_x = (mouse_x) // self.grid_obj.cell_size
        # numpy(height, width)
        return grid_y, grid_x

    def process_mouse_input(self, event, sparse_cells):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x, mouse_y)
        # If the click is on container_surface, only process it for buttons
        if not self.container_surface_rect:
            return
        # Get position relative to container_surface
        rel_x = mouse_x - (
            self.screen_width
            - self.container_surface_rect.width
            - self.buffer_space
        )
        rel_y = mouse_y - self.buffer_space

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # button event == 1 is for left click
            if self.play_button_rect.collidepoint(
                (rel_x, rel_y)
            ) or self.pause_button_rect.collidepoint((rel_x, rel_y)):
                self.is_playing = not self.is_playing
                return "is_playing", None

            elif self.reset_button_rect.collidepoint((rel_x, rel_y)):
                return "reset", None

            elif self.clear_button_rect.collidepoint((rel_x, rel_y)):
                return "clear", None

            elif self.save_button_rect.collidepoint((rel_x, rel_y)):
                return "save", None

            elif self.upload_button_rect.collidepoint((rel_x, rel_y)):
                return "load", None

            elif not (
                0 <= rel_x <= self.container_surface.get_width()
                and 0 <= rel_y <= self.container_surface.get_height()
            ):
                # Convert positional coordinates into cells
                grid_pos = self.convert_pixel_pos_to_grid(
                    mouse_y, mouse_x
                )  # height, width
                grid_y, grid_x = grid_pos

                if (  # for now, just check that ther's a padding of cells around the grid, to deal with edges
                    grid_x > 0
                    and grid_x < len(self.grid[0]) - 1
                    and grid_y > 0
                    and grid_y < len(self.grid) - 1
                ):
                    action = (
                        "remove_cell" if grid_pos in sparse_cells else "add_cell"
                    )
                    return action, grid_pos
        elif event.type == pygame.MOUSEWHEEL:
            self.count += 1
            if event.y > 0:
                self.grid_obj.zoom(zoom_in=False)
            else:
                self.grid_obj.zoom(zoom_in=True)

        return

    def draw_container(self):
        self.container_surface = pygame.Surface(
            (self.container_width, self.container_height)
        )
        self.container_surface.fill((175, 238, 238, 128))  # Semi-transparent
        self.container_surface = (
            self.container_surface.convert_alpha()
        )  # make it transparent

        self.container_surface_rect = self.container_surface.get_rect(
            topright=(self.screen_width - self.buffer_space, self.buffer_space)
        )

    def draw_buttons(self):
        # Clear the container_surface
        self.draw_container()

        if self.is_playing:
            self.container_surface.blit(
                self.pause_button, self.pause_button_rect.topleft
            )
        else:
            self.container_surface.blit(self.play_button, self.play_button_rect.topleft)

        self.container_surface.blit(self.reset_button, self.reset_button_rect.topleft)
        self.container_surface.blit(self.clear_button, self.clear_button_rect.topleft)
        self.container_surface.blit(self.save_button, self.save_button_rect.topleft)
        self.container_surface.blit(self.upload_button, self.upload_button_rect.topleft)
        # self.container_surface.blit(
        #     self.zoom_in_button, self.zoom_in_button_rect.topleft
        # )
        # self.container_surface.blit(
        #     self.zoom_out_button, self.zoom_out_button_rect.topleft
        # )

        self.screen.blit(self.container_surface, self.container_surface_rect)
