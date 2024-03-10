import pygame
from grid import Grid
from typing import Tuple, Dict


class GameControls:
    def __init__(
        self,
        screen: pygame.Surface,
    ):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        self.draw_container()

        self.is_playing = False

        self.font = pygame.font.Font(None, 18)
        self.play_button, self.play_button_rect, self.play_text_rect = self.create_button(
            "icons", "play.png", "Play", x_pos=self.container_width-80, y_pos=20
        )
        self.pause_button, self.pause_button_rect, self.pause_text_rect = self.create_button(
            "icons", "pause.png", "Pause", x_pos=self.container_width-80, y_pos=20
        )
        self.reset_button, self.reset_button_rect, self.reset_text_rect = self.create_button(
            "icons", "reset.png", "Reset", x_pos=self.container_width-80, y_pos=80
        )
        self.clear_button, self.clear_button_rect, self.clear_text_rect = self.create_button(
            "icons", "clear.png", "Clear", x_pos=self.container_width-80, y_pos=140
        )
        self.save_button, self.save_button_rect, self.save_text_rect = self.create_button(
            "icons", "save.png", "Save", x_pos=self.container_width-80, y_pos=200
        )
        self.upload_button, self.upload_button_rect, self.upload_text_rect = self.create_button(
            "icons", "upload.png", "Upload", x_pos=self.container_width-80, y_pos=260
        )

        self.next_button, self.next_button_rect, self.next_text_rect = self.create_button(
            "icons", "next.png", "Next", x_pos=self.container_width-80, y_pos=320
        )

        self.mouse_pos = (0, 0)
        self.mouse_drag = False

    @classmethod
    def laod_resource_image(cls, dir_name: str, name: str) -> pygame.Surface:
        import os
        resourse_dir = os.path.dirname(__file__)
        path = os.path.join(resourse_dir, dir_name, name)
        return pygame.image.load(path)

    # def create_button(
    #     self,
    #     dir_name: str,
    #     img_name: str,
    #     text: str,
    #     x_pos: int,
    #     y_pos: int,
    # ) -> Tuple[pygame.Surface, pygame.Rect, pygame.Rect]:
    #     img_dimension = (30, 30)
    #     button = self.laod_resource_image(dir_name, img_name)
    #     button = pygame.transform.scale(button, img_dimension)
    #     button_rect = button.get_rect()
    #     button_rect.topright = (x_pos, y_pos)

    #     # Calculate the text rect based on button dimensions
    #     text_surface = self.font.render(text, True, (255, 255, 255)) # Make text white
    #     text_rect = text_surface.get_rect()
    #     text_rect.topleft = (button_rect.left, button_rect.bottom + 10) # Position it 10 pixels below the button

    #     return button, button_rect, text_rect
    def create_button(
        self,
        dir_name: str,
        img_name: str,
        text: str,
        x_pos: int,
        y_pos: int,
    ) -> Tuple[pygame.Surface, pygame.Rect, pygame.Rect]:
        img_dimension = (30, 30)
        button = self.laod_resource_image(dir_name, img_name)
        button = pygame.transform.scale(button, img_dimension)
        button_rect = button.get_rect()
        button_rect.topright = (x_pos, y_pos)

        # Calculate the text rect based on button dimensions
        text_surface = self.font.render(text, True, (255, 255, 255)) # Make text white
        text_rect = text_surface.get_rect()
        text_rect.topleft = (button_rect.right + 10, button_rect.centery - text_rect.height // 2) # Position it 10 pixels to the right of the button

        return button, button_rect, text_rect

    def draw_container(self):
        self.buffer_space = 20
        self.container_width = self.screen_width // 8 - 2 * self.buffer_space
        self.container_height = self.screen_width // 3 - 2 * self.buffer_space

        self.container_surface = pygame.Surface(
            (self.container_width, self.container_height)
        )
        self.container_surface.fill((0, 0, 0, 0))  # fully transparent container
        self.container_surface = (
            self.container_surface.convert_alpha()
        )  # make it transparent

        self.container_surface_rect = self.container_surface.get_rect(
            topright=(self.screen_width - self.buffer_space, self.buffer_space)
        )

    def draw_buttons(self):
        # draw a clear container surface each time
        self.draw_container()

        if self.is_playing:
            self.draw_button_with_text(
                "Pause",
                self.pause_button,
                self.pause_button_rect,
                self.pause_text_rect,
            )
        else:
            self.draw_button_with_text(
                "Play",
                self.play_button,
                self.play_button_rect,
                self.play_text_rect,
            )

        self.draw_button_with_text(
            "Reset",
            self.reset_button,
            self.reset_button_rect,
            self.reset_text_rect,
        )
        self.draw_button_with_text(
            "Clear",
            self.clear_button,
            self.clear_button_rect,
            self.clear_text_rect,
        )
        self.draw_button_with_text(
            "Save",
            self.save_button,
            self.save_button_rect,
            self.save_text_rect,
        )
        self.draw_button_with_text(
            "Upload",
            self.upload_button,
            self.upload_button_rect,
            self.upload_text_rect,
        )
        self.draw_button_with_text(
            "Next",
            self.next_button,
            self.next_button_rect,
            self.next_text_rect,
        )

        self.screen.blit(
            self.container_surface, self.container_surface_rect.topleft
        )  # topleft might be removed later, just experimenting rn

    def draw_button_with_text(self, text, button, button_rect, text_rect):
        # Calculate the position and size of the button container
        container_topleft = button_rect.topleft
        container_size = (150, 150)  # setting fixed size of 100x100 pixels

        # Draw the button container
        pygame.draw.rect(
            self.container_surface, (0, 206, 209, 200),
            pygame.Rect(container_topleft, container_size)
        )

        # Draw the button
        self.container_surface.blit(button, button_rect.topleft)

        # Draw the text
        self.draw_text(text, text_rect.topleft)

    def draw_text(self, text, position):
        # Create a Surface with the text
        text_surface = self.font.render(text, True, (255, 255, 255)) # Make text white
        # Draw the text on the container surface
        self.container_surface.blit(text_surface, position)

    def process_mouse_input(
            self,
            event,
            sparse_cells: Dict[Tuple[int, int], int],
            grid: 'Grid'
    ):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if not self.container_surface_rect:
            return
        # Get position relative to container_surface
        rel_x = mouse_x - (
            self.screen_width
            - self.container_surface_rect.width
            - self.buffer_space
        )
        rel_y = mouse_y - self.buffer_space

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_drag = True
            self.mouse_pos = (mouse_x, mouse_y)

            if self.play_button_rect.collidepoint(
                (rel_x, rel_y)
            ) or self.pause_button_rect.collidepoint((rel_x, rel_y)):
                self.is_playing = not self.is_playing
                return "is_playing", None

            elif self.reset_button_rect.collidepoint((rel_x, rel_y)):
                return "reset", None

            elif self.clear_button_rect.collidepoint((rel_x, rel_y)):
                return "clear", None

            elif self.next_button_rect.collidepoint((rel_x, rel_y)):
                return "next_state", None

            elif self.save_button_rect.collidepoint((rel_x, rel_y)):
                return "save", None

            elif self.upload_button_rect.collidepoint((rel_x, rel_y)):
                return "load", None

            elif not (
                0 <= rel_x <= self.container_surface.get_width()
                and 0 <= rel_y <= self.container_surface.get_height()
            ):
                # Convert positional coordinates into cells
                grid_y = ((self.mouse_pos[1] - grid.camera_y) // grid.adjusted_cell_size)
                grid_x = ((self.mouse_pos[0] - grid.camera_x) // grid.adjusted_cell_size)
                pos = grid_y, grid_x

                action = (
                    "remove_cell" if pos in sparse_cells else "add_cell"
                )
                return action, pos

        elif self.mouse_drag and event.type == pygame.MOUSEMOTION:
            new_mouse_pos = event.pos
            dx = new_mouse_pos[0] - self.mouse_pos[0]
            dy = new_mouse_pos[1] - self.mouse_pos[1]

            self.mouse_pos = new_mouse_pos
            delta = (dx, dy)

            return "panning", delta

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_drag = False

        elif event.type == pygame.MOUSEWHEEL:
            grid.mouse_pos = (mouse_x, mouse_y)
            # passing event.y for vertical and event.x for horizontal scroll
            return 'viewpoint', event.y
        return
