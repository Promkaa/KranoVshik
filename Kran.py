import pygame
import sys
import random
import cv2
from pathlib import Path

# Инициализация Pygame
pygame.init()

# Установка логотипа
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)

# Настройки экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крановщик")

# Цвета
BLUE = (135, 206, 250)  # Синий фон по умолчанию
BLACK = (0, 0, 0)  # Цвет текста и кнопок
WHITE = (255, 255, 255)  # Цвет текста кнопок
CRANE_COLOR = (255, 165, 0)  # Оранжевый цвет для крана

# Настройки игры
FPS = 60
clock = pygame.time.Clock()

# Размеры объектов
LADDER_WIDTH = 20
LADDER_HEIGHT = SCREEN_HEIGHT
RUNG_SPACING = 40  # Расстояние между перекладинами
BIRD_SIZE = 100
CRANE_SIZE = 150

# Загрузка изображений
def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

# Попытка загрузить пользовательский фон
try:
    background_image = pygame.image.load("image/backgrounds/backgroundcutscene2.png").convert()  # Замените "background.png" на путь к вашему файлу
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH*3, SCREEN_HEIGHT))  # Масштабируем фон
    use_background_image = True
except FileNotFoundError:
    use_background_image = False  # Если файл не найден, используем цвет по умолчанию

# Игрок
player_image = load_image("image/icon.png", (70, 70))  # Замените "player.png" на свой файл
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
bird_image = load_image("image/tuchi/tucha1.png", (BIRD_SIZE+100, BIRD_SIZE-50))  # Замените "bird.png" на свой файл

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

# Главное меню
def main_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render("Крановщик", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    button_font = pygame.font.Font(None, 50)
    start_button = button_font.render("Начать игру", True, WHITE)
    quit_button = button_font.render("Выйти", True, WHITE)

    start_button_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    quit_button_rect = quit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    while True:
        screen.fill(BLUE)
        screen.blit(title_text, title_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(quit_button, quit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    play_intro()
                    game_loop(
                        bird_spawn_timer=0,
                        crane_color=CRANE_COLOR,
                        crane=crane
                    )  # Передаем необходимые параметры
                    return
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# Воспроизведение видео-интро
def play_intro():
    video_path = Path("intro.mp4")  # Путь к видеофайлу в корневой папке
    if not video_path.exists():
        return  # Если видео не найдено, пропускаем интро

    cap = cv2.VideoCapture(str(video_path))
    success, frame = cap.read()
    skip_intro = False

    while success and not skip_intro:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    skip_intro = True  # Пропустить интро при нажатии "вверх" или "вниз"

        clock.tick(30)  # Ограничение FPS для видео
        success, frame = cap.read()

    cap.release()

# Основной цикл игры
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

# Запуск игры
if __name__ == "__main__":
    main_menu()
