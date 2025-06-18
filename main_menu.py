from button import *
import sys
from config import *
from difficult import difficulty_menu

def main_menu(resources):
    """Главное меню"""
    print("Запуск главного меню...")

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
    resources['bg_main_music'].stop()
    resources['bg_menu_music'].play(-1)  # Зацикленное воспроизведение

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Выход из игры через крестик")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                if event.button == play_button:
                    print("Нажата кнопка 'Играть'")
                    # Остановка музыки меню перед переходом в игру
                    resources['bg_menu_music'].stop()
                    resources['bg_main_music'].play(-1)
                    # Показываем меню выбора сложности
                    difficulty = difficulty_menu(resources)
                    if difficulty is not None:
                        return 'game', difficulty
                    else:
                        resources['bg_main_music'].stop()
                        # Если вернулись назад, снова включаем музыку
                        resources['bg_menu_music'].play(-1)
                elif event.button == exit_button:
                    print("Нажата кнопка 'Выход'")
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
        bg_frame = resources['background'][(pygame.time.get_ticks() // BG_ANIMATION_SPEED) % len(resources['background'])]
        screen.blit(bg_frame, (0, 0))
        play_button.draw(screen)
        exit_button.draw(screen)

        # Обновление состояний
        mouse_pos = pygame.mouse.get_pos()
        play_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)
