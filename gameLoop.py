import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, screen, BLACK, BLUE, FPS, clock
from player import player_image, player_speed, player
from ladder import ladder_rect, ladder_image
from bird import birds, bird_speed, bird_spawn_delay, spawn_bird, bird_image_left, bird_image_right
from check import check_collision, check_reach_crane
import sys


try:
    background_image = pygame.image.load("image/backgrounds/backgroundcutscene2.png").convert()  # Замените "background.png" на путь к вашему файлу
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH*3, SCREEN_HEIGHT))  # Масштабируем фон
    use_background_image = True
except FileNotFoundError:
    use_background_image = False  # Если файл не найден, используем цвет по умолчанию

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
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if not game_over and not game_won:
            if keys[pygame.K_UP]:
                if ladder_rect.top <= player.y and ladder_rect.bottom >= player.y:  # Проверяем, находится ли игрок на лестнице
                    player.y -= player_speed
            if keys[pygame.K_DOWN]:
                if ladder_rect.top <= player.y and ladder_rect.bottom >= player.y:  # Проверяем, находится ли игрок на лестнице
                    player.y += player_speed


        # Логика появления птиц
        bird_spawn_timer += clock.get_time()
        if bird_spawn_timer >= bird_spawn_delay:
            spawn_bird(bird_image_left, bird_image_right, birds)
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
        if ladder_image:  # Если изображение лестницы загружено
            screen.blit(ladder_image, ladder_rect)
        else:  # Если изображение не загружено, отрисовываем простую лестницу
            pygame.draw.rect(screen, BLACK, ladder_rect)

        # Игрок
        screen.blit(player_image, player)

        # Птицы
        for bird in birds:
            screen.blit(bird["image"], bird["rect"])  # Используем изображение, назначенное для каждой птицы

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
