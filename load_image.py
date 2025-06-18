import pygame
import os


def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

def load_images(folder):
    return [pygame.image.load(os.path.join(folder, img)).convert_alpha()
            for img in sorted(os.listdir(folder)) if img.endswith(".png")]