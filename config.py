import pygame


# Константы
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BG_ANIMATION_SPEED = 100
ANIMATION_SPEED = 15
FPS = 60
# Цвета
BLUE = (135, 206, 250)  # Синий фон по умолчанию
BLACK = (0, 0, 0)  # Цвет текста и кнопок
WHITE = (255, 255, 255)  # Цвет текста кнопок
CRANE_COLOR = (255, 165, 0)  # Оранжевый цвет для крана

# Размеры объектов
LADDER_WIDTH = 20
LADDER_HEIGHT = SCREEN_HEIGHT
RUNG_SPACING = 40  # Расстояние между перекладинами
BIRD_SIZE = 100
CRANE_SIZE = 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
crane = pygame.Rect(SCREEN_WIDTH // 2 - CRANE_SIZE // 2, -CRANE_SIZE, CRANE_SIZE, CRANE_SIZE)