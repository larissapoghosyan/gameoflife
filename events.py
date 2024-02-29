import pygame
from typing import Dict, Tuple, Callable

STEP_EVENT = pygame.USEREVENT


# class Event:

#     def __init__(self):
#         self.listeners = []

#     def trigger_event(self, data: Dict[Tuple[int, int], int]):
#         for listener in self.listeners:
#             listener(data)

#     def add_listener(
#             self,
#             listener: Callable[[Dict[Tuple[int, int], int]], None]
#     ):
#         self.listeners.append(listener)
