import pygame
from pathlib import Path
from config import SCREEN_HEIGHT, SCREEN_WIDTH, screen
from loadSprite import load_sprite_sheets



def show_loading_screen():
    """Отображение экрана загрузки"""
    font = pygame.font.Font(None, 36)
    text = font.render("Загрузка...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    progress_bar = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, 400, 30)
    fill_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, 400, 30)

    screen.fill((10, 10, 10))
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, (255, 255, 255), progress_bar, 2)
    pygame.display.flip()

    return fill_rect

def update_progress(fill_rect, progress):
    """Обновление прогресс-бара"""
    if progress > 1.0:
        progress = 1.0
    fill_rect.width = 400 * progress
    pygame.draw.rect(screen, (0, 255, 0), fill_rect)
    pygame.display.flip()
    pygame.time.wait(10)
    pygame.event.pump()

def load_resources():
    """Загрузка всех ресурсов с анимацией прогресса"""
    fill_rect = show_loading_screen()

    # Загрузка фона
    background = load_sprite_sheets('image/backgrounds/background_sprites_main_menu',
                                    lambda p: update_progress(fill_rect, p * 0.4))

    # Загрузка изображений кнопок
    play = pygame.transform.scale(pygame.image.load('image/button/play.png'), (200, 80))
    update_progress(fill_rect, 0.45)

    play_hover = pygame.transform.scale(pygame.image.load('image/button/play_hover.png'), (200, 80))
    update_progress(fill_rect, 0.5)

    exit_btn = pygame.transform.scale(pygame.image.load('image/button/exit.png'), (200, 80))
    update_progress(fill_rect, 0.55)

    exit_hover = pygame.transform.scale(pygame.image.load('image/button/exit_hover.png'), (200, 80))
    update_progress(fill_rect, 0.6)

    # Загрузка звука
    click_sound = pygame.mixer.Sound('sounds/click.mp3')
    update_progress(fill_rect, 0.65)

    # Проверка наличия видеоинтро
    intro_exists = Path("intro.mp4").exists()
    update_progress(fill_rect, 1.0)

    return {
        'background': background,
        'play': play,
        'play_hover': play_hover,
        'exit': exit_btn,
        'exit_hover': exit_hover,
        'click_sound': click_sound,
        'has_intro': intro_exists,
        'bg_menu_music': pygame.mixer.Sound('music/background_menu_music.mp3')
    }
