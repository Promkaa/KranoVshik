import pygame
from loadIMG import load_image
from config import SCREEN_HEIGHT, SCREEN_WIDTH, LADDER_HEIGHT, LADDER_WIDTH

# Лестница
ladder_image_path = "image/ladder.png"  # Путь к изображению лестницы
try:
    ladder_image = load_image(ladder_image_path, ()) # в пустых скобках размеры лестницы, изменить, как будет лестница
    ladder_rect = ladder_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
except FileNotFoundError:
    ladder_image = None
    ladder_rect = pygame.Rect(SCREEN_WIDTH // 2 - LADDER_WIDTH // 2, 0, LADDER_WIDTH, LADDER_HEIGHT)
