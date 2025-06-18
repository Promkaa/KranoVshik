from config import *
from button import ImageButton
import sys

def get_difficulty_settings(difficulty):
    """Возвращает настройки сложности в зависимости от выбранного уровня"""
    if difficulty == DIFFICULTY_EASY:
        return {
            'eagle_spawn_range': (BASE_EAGLE_SPAWN_RANGE[0] * 2, BASE_EAGLE_SPAWN_RANGE[1] * 2),
            'eagle_speed_range': (BASE_EAGLE_SPEED_RANGE[0] * 0.7, BASE_EAGLE_SPEED_RANGE[1] * 0.7),
            'max_eagles': BASE_MAX_EAGLES - 1,

            'helicopter_spawn_range': (BASE_HELICOPTER_SPAWN_RANGE[0] * 2, BASE_HELICOPTER_SPAWN_RANGE[1] * 2),
            'helicopter_speed_range': (BASE_HELICOPTER_SPEED_RANGE[0] * 0.7, BASE_HELICOPTER_SPEED_RANGE[1] * 0.7),
            'max_helicopters': BASE_MAX_HELICOPTERS - 1,

            'ufo_spawn_range': (BASE_UFO_SPAWN_RANGE[0] * 3, BASE_UFO_SPAWN_RANGE[1] * 3),
            'ufo_speed_range': (BASE_UFO_SPEED_RANGE[0] * 0.6, BASE_UFO_SPEED_RANGE[1] * 0.6),
            'max_ufos': 0,  # Нет НЛО на легком уровне
            'ufo_chaos_factor': BASE_UFO_CHAOS_FACTOR * 0.7,

            'brick_spawn_range': (BASE_BRICK_SPAWN_RANGE[0] * 2, BASE_BRICK_SPAWN_RANGE[1] * 2),
            'brick_speed_range': (BASE_BRICK_SPEED_RANGE[0] * 0.8, BASE_BRICK_SPEED_RANGE[1] * 0.8),
            'max_bricks': BASE_MAX_BRICKS - 1
        }
    elif difficulty == DIFFICULTY_NORMAL:
        return {
            'eagle_spawn_range': BASE_EAGLE_SPAWN_RANGE,
            'eagle_speed_range': BASE_EAGLE_SPEED_RANGE,
            'max_eagles': BASE_MAX_EAGLES,

            'helicopter_spawn_range': BASE_HELICOPTER_SPAWN_RANGE,
            'helicopter_speed_range': BASE_HELICOPTER_SPEED_RANGE,
            'max_helicopters': BASE_MAX_HELICOPTERS,

            'ufo_spawn_range': BASE_UFO_SPAWN_RANGE,
            'ufo_speed_range': BASE_UFO_SPEED_RANGE,
            'max_ufos': BASE_MAX_UFOS,
            'ufo_chaos_factor': BASE_UFO_CHAOS_FACTOR,

            'brick_spawn_range': BASE_BRICK_SPAWN_RANGE,
            'brick_speed_range': BASE_BRICK_SPEED_RANGE,
            'max_bricks': BASE_MAX_BRICKS
        }
    elif difficulty == DIFFICULTY_HARD:
        return {
            'eagle_spawn_range': (BASE_EAGLE_SPAWN_RANGE[0] * 0.5, BASE_EAGLE_SPAWN_RANGE[1] * 0.5),
            'eagle_speed_range': (BASE_EAGLE_SPEED_RANGE[0] * 1.5, BASE_EAGLE_SPEED_RANGE[1] * 1.5),
            'max_eagles': BASE_MAX_EAGLES + 1,

            'helicopter_spawn_range': (BASE_HELICOPTER_SPAWN_RANGE[0] * 0.5, BASE_HELICOPTER_SPAWN_RANGE[1] * 0.5),
            'helicopter_speed_range': (BASE_HELICOPTER_SPEED_RANGE[0] * 1.4, BASE_HELICOPTER_SPEED_RANGE[1] * 1.4),
            'max_helicopters': BASE_MAX_HELICOPTERS + 1,

            'ufo_spawn_range': (BASE_UFO_SPAWN_RANGE[0] * 0.5, BASE_UFO_SPAWN_RANGE[1] * 0.5),
            'ufo_speed_range': (BASE_UFO_SPEED_RANGE[0] * 1.5, BASE_UFO_SPEED_RANGE[1] * 1.5),
            'max_ufos': BASE_MAX_UFOS + 1,
            'ufo_chaos_factor': BASE_UFO_CHAOS_FACTOR * 1.3,
            'ufo_warning_time': BASE_UFO_WARNING_TIME * 0.7,
            'ufo_death_light_time': BASE_UFO_DEATH_LIGHT_TIME * 1.2,

            'brick_spawn_range': (BASE_BRICK_SPAWN_RANGE[0] * 0.5, BASE_BRICK_SPAWN_RANGE[1] * 0.5),
            'brick_speed_range': (BASE_BRICK_SPEED_RANGE[0] * 1.3, BASE_BRICK_SPEED_RANGE[1] * 1.3),
            'max_bricks': BASE_MAX_BRICKS + 1
        }

def difficulty_menu(resources):
    """Меню выбора сложности"""
    print("Запуск меню выбора сложности...")

    easy_button = ImageButton(
        x= 50, y=250,
        width=396, height=108,
        image=resources['easy'],
        hover_image=resources['easy_hover'],
        sound=resources['click_sound']
    )

    normal_button = ImageButton(
        x= 50, y=400,
        width=396, height=108,
        image=resources['normal'],
        hover_image=resources['normal_hover'],
        sound=resources['click_sound']
    )

    hard_button = ImageButton(
        x= 50, y=550,
        width=396, height=108,
        image=resources['hard'],
        hover_image=resources['hard_hover'],
        sound=resources['click_sound']
    )

    back_button = ImageButton(
        x= 50, y=700,
        width=396, height=108,
        image=resources['exit'],
        hover_image=resources['exit_hover'],
        sound=resources['click_sound']
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                if event.button == easy_button:
                    print("Выбрана легкая сложность")
                    return DIFFICULTY_EASY
                elif event.button == normal_button:
                    print("Выбрана нормальная сложность")
                    return DIFFICULTY_NORMAL
                elif event.button == hard_button:
                    print("Выбрана сложная сложность")
                    return DIFFICULTY_HARD
                elif event.button == back_button:
                    print("Назад в главное меню")
                    return None
            else:
                easy_button.handle_event(event)
                normal_button.handle_event(event)
                hard_button.handle_event(event)
                back_button.handle_event(event)

        # Отрисовка
        bg_frame = resources['background'][
            (pygame.time.get_ticks() // BG_ANIMATION_SPEED) % len(resources['background'])
            ]
        screen.blit(bg_frame, (0, 0))

        # Текст заголовка
        font = pygame.font.Font(None, 56)
        title = font.render("Выберите сложность", True, (255, 255, 255))
        screen.blit(title, (50, 150))

        # Кнопки
        easy_button.draw(screen)
        normal_button.draw(screen)
        hard_button.draw(screen)
        back_button.draw(screen)

        # Обновление состояний
        mouse_pos = pygame.mouse.get_pos()
        easy_button.check_hover(mouse_pos)
        normal_button.check_hover(mouse_pos)
        hard_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)
