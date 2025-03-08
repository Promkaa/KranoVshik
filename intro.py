import pygame
import sys
import cv2
from pathlib import Path
from config import SCREEN_HEIGHT, SCREEN_WIDTH, screen, clock

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