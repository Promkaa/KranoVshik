import random
from config import BIRD_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from loadIMG import load_image

birds = []
bird_spawn_timer = 0
bird_spawn_delay = 1000  # В миллисекундах
bird_speed = 3
bird_image_left = load_image("image/tuchi/tucha1.png", (BIRD_SIZE + 100, BIRD_SIZE - 50))  # Птица летит справа налево
bird_image_right = pygame.transform.flip(bird_image_left, True, False)  # Отразим изображение для птицы, летящей слева направо

def spawn_bird(bird_image_left, bird_image_right, birds):
    bird_x = random.choice([-BIRD_SIZE, SCREEN_WIDTH])
    bird_y = random.randint(0, SCREEN_HEIGHT - BIRD_SIZE)
    bird_direction = 1 if bird_x < 0 else -1  # Определяем направление полета
    bird_image = bird_image_right if bird_direction == 1 else bird_image_left  # Выбираем изображение
    birds.append({"rect": pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE),
                  "direction": bird_direction,
                  "image": bird_image})  # Добавляем изображение к птице