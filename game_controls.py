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

        self.mouse_drag = False
        self.mouse_pos = (0, 0)

    @classmethod
    def laod_resource_image(cls, dir_name: str, name: str) -> pygame.Surface:
        import os
        resourse_dir = os.path.dirname(__file__)
        path = os.path.join(resourse_dir, dir_name, name)
        return pygame.image.load(path)

    @classmethod
    def create_button(
        cls,
        dir_name: str,
        img_name: str,
        x_pos: int,
        y_pos: int,
    ) -> Tuple[pygame.Surface, pygame.Rect]:
        img_dimension = (30, 30)
        button = cls.laod_resource_image(dir_name, img_name)
        button = pygame.transform.scale(button, img_dimension)
        button_rect = button.get_rect()
        button_rect.topright = (x_pos, y_pos)
        return button, button_rect

    def draw_container(self):
        self.buffer_space = 10
        self.container_width = self.screen_width // 7 - 2 * self.buffer_space
        self.container_height = self.screen_width // 4 - 2 * self.buffer_space

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
        # draw a clear contianer surface each time
        self.draw_container()

        if self.is_playing:
            self.container_surface.blit(
                self.pause_button, self.pause_button_rect.topleft
            )
        else:
            self.container_surface.blit(
                self.play_button, self.play_button_rect.topleft
            )
        self.container_surface.blit(
            self.reset_button, self.reset_button_rect.topleft
        )
        self.container_surface.blit(
            self.clear_button, self.clear_button_rect.topleft
        )
        self.container_surface.blit(
            self.save_button, self.save_button_rect.topleft
        )
        self.container_surface.blit(
            self.upload_button, self.upload_button_rect.topleft
        )

        self.screen.blit(
            self.container_surface, self.container_surface_rect.topleft
        )  # topleft might be removed later, just experimenting rn

    def convert_pixel_coords_to_game_coords(self, mouse_x, mouse_y):
        pass

    def process_mouse_input(
            self,
            event,
            sparse_cells: Dict[Tuple[int, int], int],
            grid: 'Grid'
    ):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.container_surface_rect:
            # Get position relative to container_surface
            rel_x = mouse_x - (
                self.screen_width
                - self.container_surface_rect.width
                - self.buffer_space
            )
            rel_y = mouse_y - self.buffer_space

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # f(mouse_y, mouse_x)

                if self.play_button_rect.collidepoint(
                    (rel_x, rel_y)
                ) or self.pause_button_rect.collidepoint((rel_x, rel_y)):
                    self.is_playing = not self.is_playing
                    return "is_playing", None
                elif self.upload_button_rect.collidepoint((rel_x, rel_y)):
                    return "load", None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_drag = True
            self.mouse_pos = (mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_drag = False

        elif self.mouse_drag and event.type == pygame.MOUSEMOTION:
            new_mouse_pos = event.pos
            dx = new_mouse_pos[0] - self.mouse_pos[0]
            dy = new_mouse_pos[1] - self.mouse_pos[1]

            self.mouse_pos = new_mouse_pos
            delta = (dx, dy)

            return "panning", delta

        elif event.type == pygame.MOUSEWHEEL:
            grid.mouse_pos = (mouse_x, mouse_y)
            # passing event.y for vertical and event.x for horizontal scroll
            return 'viewpoint', event.y
        return
