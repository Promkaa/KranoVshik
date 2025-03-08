import pygame
from loadIMG import load_image
from config import SCREEN_WIDTH, SCREEN_HEIGHT

player_image = load_image("image/icon.png", (70, 70))  # Замените "player.png" на свой файл
player = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 50, 40, 40)
player_speed = 5