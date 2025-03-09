import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, map_width, map_height):
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, rect):
        """Преобразует координаты объекта с учетом камеры"""
        return rect.move(-self.rect.x, -self.rect.y)

    def update(self, target):
        """Обновляет позицию камеры относительно цели"""
        # Новые координаты камеры (без инверсии знака)
        x = target.x + target.width // 2 - SCREEN_WIDTH // 2
        y = target.y + target.height // 2 - SCREEN_HEIGHT // 2

        # Ограничение перемещения камеры в пределах карты
        x = max(0, min(self.map_width - SCREEN_WIDTH, x))
        y = max(0, min(self.map_height - SCREEN_HEIGHT, y))

        self.rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)