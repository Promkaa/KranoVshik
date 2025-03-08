import pygame
import sys
import os
import cv2
from pathlib import Path
from button import ImageButton
import random

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

# Инициализация
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Установка логотипа и названия
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Крановщик")

def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

try:
    background_image = pygame.image.load("image/backgrounds/backgroundcutscene2.png").convert()  # Замените "background.png" на путь к вашему файлу
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH*3, SCREEN_HEIGHT))  # Масштабируем фон
    use_background_image = True
except FileNotFoundError:
    use_background_image = False  # Если файл не найден, используем цвет по умолчанию

# Игрок
player_image = load_image("images/icon.png", (70, 70))  # Замените "player.png" на свой файл
player = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 50, 40, 40)
player_speed = 5

# Лестница
ladder_left = pygame.Rect(SCREEN_WIDTH // 2 - LADDER_WIDTH // 2 - 10, 0, 10, LADDER_HEIGHT)
ladder_right = pygame.Rect(SCREEN_WIDTH // 2 + LADDER_WIDTH // 2, 0, 10, LADDER_HEIGHT)
rungs = []  # Перекладины
for i in range(0, SCREEN_HEIGHT, RUNG_SPACING):
    rungs.append(pygame.Rect(ladder_left.x, i, LADDER_WIDTH, 5))

# Кран
crane = pygame.Rect(SCREEN_WIDTH // 2 - CRANE_SIZE // 2, -CRANE_SIZE, CRANE_SIZE, CRANE_SIZE)
# Птицы
birds = []
bird_spawn_timer = 0
bird_spawn_delay = 1000  # В миллисекундах
bird_speed = 3
bird_image = load_image("images/tuchi/tucha1.png", (BIRD_SIZE+100, BIRD_SIZE-50))  # Замените "bird.png" на свой файл

def spawn_bird():
    bird_x = random.choice([-BIRD_SIZE, SCREEN_WIDTH])
    bird_y = random.randint(0, SCREEN_HEIGHT - BIRD_SIZE)
    bird_direction = 1 if bird_x < 0 else -1
    birds.append({"rect": pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE), "direction": bird_direction})

# Функция для проверки столкновений
def check_collision():
    for bird in birds:
        if player.colliderect(bird["rect"]):
            return bird["direction"], bird["rect"].center  # Возвращаем направление птицы и её центр
    return None, None

# Проверка достижения крана
def check_reach_crane():
    return player.colliderect(crane)

def load_sprite_sheets(folder_path, progress_callback):
    """Загрузка спрайтов фона с отображением прогресса"""
    frames = []
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
    total = len(files)
    for i, file in enumerate(files):
        img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frames.append(img)
        progress_callback((i + 1) / total)
    return frames


def show_loading_screen():
    """Отображение экрана загрузки"""
    font = pygame.font.Font(None, 36)
    text = font.render("Загрузка...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    progress_bar = pygame.Rect(200, 400, 400, 30)
    fill_rect = pygame.Rect(200, 400, 0, 30)

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
    background = load_sprite_sheets('image/background_sprites/background_sprites_main_menu',
                                    lambda p: update_progress(fill_rect, p * 0.4))

    # Загрузка изображений кнопок
    play = pygame.transform.scale(pygame.image.load('image/buttons/play.png'), (200, 80))
    update_progress(fill_rect, 0.45)

    play_hover = pygame.transform.scale(pygame.image.load('image/buttons/play_hover.png'), (200, 80))
    update_progress(fill_rect, 0.5)

    exit_btn = pygame.transform.scale(pygame.image.load('image/buttons/exit.png'), (200, 80))
    update_progress(fill_rect, 0.55)

    exit_hover = pygame.transform.scale(pygame.image.load('image/buttons/exit_hover.png'), (200, 80))
    update_progress(fill_rect, 0.6)

    # Загрузка звука
    click_sound = pygame.mixer.Sound('music/click.mp3')
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


def play_intro():
    """Воспроизведение видео-интро"""
    video_path = Path("intro.mp4")
    if not video_path.exists():
        return

    cap = cv2.VideoCapture(str(video_path))
    success, frame = cap.read()
    skip_sound = pygame.mixer.Sound('sounds/click.mp3')
    font = pygame.font.Font(None, 24)
    blink_interval = 500
    last_blink = 0
    blink_visible = True

    while success:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip_sound.play()
                    cap.release()
                    return

        # Мерцание подсказки
        if current_time - last_blink > blink_interval:
            blink_visible = not blink_visible
            last_blink = current_time

        # Отрисовка кадра
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        # Подсказка пропуска
        if blink_visible:
            skip_text = font.render("Нажмите ПРОБЕЛ для пропуска", True, (255, 255, 255))
            screen.blit(skip_text, (SCREEN_WIDTH - skip_text.get_width() - 20, SCREEN_HEIGHT - 40))

        pygame.display.flip()
        clock.tick(30)
        success, frame = cap.read()

    cap.release()


def main_menu(resources):
    """Главное меню"""
    play_button = ImageButton(
        x=-200, y=250,
        width=396, height=108,
        image=resources['play'],
        hover_image=resources['play_hover'],
        sound=resources['click_sound']
    )


    exit_button = ImageButton(
        x=-200, y=400,
        width=396, height=108,
        image=resources['exit'],
        hover_image=resources['exit_hover'],
        sound=resources['click_sound']
    )

    TARGET_X = 50
    resources['bg_menu_music'].play(-1)  # Зацикленное воспроизведение
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                if event.button == play_button:
                    return 'intro' if resources['has_intro'] else 'game'
                elif event.button == exit_button:
                    pygame.quit()
                    sys.exit()
            else:
                play_button.handle_event(event)
                exit_button.handle_event(event)

        # Анимация кнопок
        if play_button.rect.x < TARGET_X:
            play_button.rect.x += ANIMATION_SPEED
        if exit_button.rect.x < TARGET_X:
            exit_button.rect.x += ANIMATION_SPEED

        # Отрисовка
        bg_frame = resources['background'][
            (pygame.time.get_ticks() // BG_ANIMATION_SPEED) %
            len(resources['background'])
            ]
        screen.blit(bg_frame, (0, 0))
        play_button.draw(screen)
        exit_button.draw(screen)

        # Обновление состояний
        mouse_pos = pygame.mouse.get_pos()
        play_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)



LADDER_WIDTH = 20
LADDER_HEIGHT = SCREEN_HEIGHT
RUNG_SPACING = 40  # Расстояние между перекладинами
BIRD_SIZE = 100
CRANE_SIZE = 150

def game_loop(bird_spawn_timer, crane_color, crane):
    running = True
    game_over = False
    game_won = False
    collision_direction = None  # Направление столкновения
    collision_center = None  # Центр птицы, с которой столкнулись
    carry_duration = 0  # Время, пока игрок уносится птицей

    while running:
        # Отрисовка фона
        if use_background_image:
            screen.blit(background_image, (0, 0))  # Используем пользовательский фон
        else:
            screen.fill(BLUE)  # Заливка экрана синим цветом, если фон не загружен

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Логика движения игрока
        keys = pygame.key.get_pressed()
        if not game_over and not game_won:
            if keys[pygame.K_UP]:
                for rung in rungs:
                    if player.bottom >= rung.top and player.top <= rung.bottom:
                        player.y -= player_speed
                        break
            if keys[pygame.K_DOWN]:
                for rung in rungs:
                    if player.top <= rung.bottom and player.bottom >= rung.top:
                        player.y += player_speed
                        break

        # Логика появления птиц
        bird_spawn_timer += clock.get_time()
        if bird_spawn_timer >= bird_spawn_delay:
            spawn_bird()
            bird_spawn_timer = 0

        # Движение птиц
        for bird in birds[:]:
            bird["rect"].x += bird["direction"] * bird_speed
            if bird["rect"].right < 0 or bird["rect"].left > SCREEN_WIDTH:
                birds.remove(bird)

        # Проверка столкновений
        collision_dir, collision_center = check_collision()
        if collision_dir is not None and carry_duration == 0:  # Если столкновение произошло
            game_over = True
            carry_duration = 10000  # Время, пока игрок уносится птицей (в миллисекундах)
        if carry_duration > 0:  # Анимация уноса
            if collision_dir == 1:  # Птица летит вправо
                player.x += bird_speed * 2
            elif collision_dir == -1:  # Птица летит влево
                player.x -= bird_speed * 2
            carry_duration -= clock.get_time()  # Уменьшаем время уноса
            if carry_duration <= 0:  # Если время истекло, завершаем игру
                game_over = True

        # Проверка достижения крана
        if not game_over and check_reach_crane():
            game_won = True

        # Отрисовка объектов
        # Лестница
        pygame.draw.rect(screen, BLACK, ladder_left)
        pygame.draw.rect(screen, BLACK, ladder_right)
        for rung in rungs:
            pygame.draw.rect(screen, BLACK, rung)

        # Игрок
        screen.blit(player_image, player)

        # Птицы
        for bird in birds:
            screen.blit(bird_image, bird["rect"])

        # Кран
        pygame.draw.rect(screen, crane_color, crane)

        # Сообщения
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game over...", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        elif game_won:
            font = pygame.font.Font(None, 74)
            text = font.render("сигареты забыл...", True, (1, 55, 32))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)


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