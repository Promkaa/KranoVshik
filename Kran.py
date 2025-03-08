import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, CRANE_COLOR, CRANE_SIZE, crane
from intro import play_intro
from loadScreen import load_resources
from gameLoop import game_loop
from Menu import main_menu

# Инициализация
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Установка логотипа и названия
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Крановщик")


if __name__ == "__main__":
    # Загрузка ресурсов
    resources = load_resources()

    # Основной цикл состояний
    state = 'main_menu'
    while True:
        if state == 'main_menu':
            state = main_menu(resources)
        elif state == 'intro':
            play_intro()
            state = 'game_loop'
        elif state == 'game_loop':
            game_loop(bird_spawn_timer=0,
                      crane_color=CRANE_COLOR,
                      crane=crane)
            state = 'main_menu'