from load_image import load_image
from load_sprite import load_sprite_sheets
from config import *

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
    play = load_image('image/button/play.png', (200, 80))
    update_progress(fill_rect, 0.45)

    play_hover = load_image('image/button/play_hover.png', (200, 80))
    update_progress(fill_rect, 0.5)

    exit_btn = load_image('image/button/exit.png', (200, 80))
    update_progress(fill_rect, 0.55)

    exit_hover = load_image('image/button/exit_hover.png', (200, 80))
    update_progress(fill_rect, 0.6)

    # Загрузка кнопок сложности
    easy_btn = load_image('image/button/easy.png', (200, 80))
    update_progress(fill_rect, 0.65)

    easy_hover = load_image('image/button/easy_hover.png', (200, 80))
    update_progress(fill_rect, 0.7)

    normal_btn = load_image('image/button/normal.png', (200, 80))
    update_progress(fill_rect, 0.75)

    normal_hover = load_image('image/button/normal_hover.png', (200, 80))
    update_progress(fill_rect, 0.8)

    hard_btn = load_image('image/button/hard.png', (200, 80))
    update_progress(fill_rect, 0.85)

    hard_hover = load_image('image/button/hard_hover.png', (200, 80))
    update_progress(fill_rect, 0.9)

    # Загрузка звука
    click_sound = pygame.mixer.Sound('sounds/click.mp3')
    update_progress(fill_rect, 0.95)

    # Проверка наличия видеоинтро

    update_progress(fill_rect, 1.0)

    return {
        'background': background,
        'play': play,
        'play_hover': play_hover,
        'exit': exit_btn,
        'exit_hover': exit_hover,
        'easy': easy_btn,
        'easy_hover': easy_hover,
        'normal': normal_btn,
        'normal_hover': normal_hover,
        'hard': hard_btn,
        'hard_hover': hard_hover,
        'click_sound': click_sound,

        'bg_menu_music': pygame.mixer.Sound('music/background_menu_music.mp3'),
        'bg_main_music': pygame.mixer.Sound('music/main_music.mp3')
    }
