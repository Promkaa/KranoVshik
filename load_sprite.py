from config import *
import os

def load_sprite_sheets(folder_path, progress_callback=None):
    """Загрузка спрайтов фона с отображением прогресса"""
    frames = []
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
    total = len(files)
    for i, file in enumerate(files):
        img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frames.append(img)
        if progress_callback:
            progress_callback((i + 1) / total)
    return frames