import sys
from difficult import *
from load_image import *
from button import *
import random

def main_game(difficulty=DIFFICULTY_NORMAL):
    """Основная игровая функция с финалом"""
    try:
        # Загружаем настройки сложности
        difficulty_settings = get_difficulty_settings(difficulty)

        # Константы для финала
        FINAL_MIN_X = 672  # Минимальная X-координата для активации финала
        FINAL_MAX_X = 1242  # Максимальная X-координата для активации финала
        FINAL_Y = 700  # Y-координата финала
        FINAL_IMAGE_PATH = "image/system/final_screen.png"  # Путь к изображению финала


        # Новое состояние игры
        STATE_FINAL = 4

        # Загрузка ресурсов игры
        background = pygame.image.load("image/backgrounds/big_background.png").convert()
        bg_width, bg_height = background.get_size()

        walk_images = load_images("image/GG")
        eagle_images = load_images("image/Eagle")
        eagle_images_flipped = [pygame.transform.flip(img, True, False) for img in eagle_images]
        helicopter_images = load_images("image/Helicopter")
        helicopter_images_flipped = [pygame.transform.flip(img, True, False) for img in helicopter_images]
        ufo_images = load_images("image/UFO")
        ufo_images_flipped = [pygame.transform.flip(img, True, False) for img in ufo_images]
        brick_images = load_images("image/Brick")
        capture_images = load_images("image/zaxvat")
        death_screen = pygame.image.load("image/deathscene/deathbirds.png").convert_alpha()
        death_screen_birds = pygame.image.load("image/deathscene/deathbirds.png").convert_alpha()
        death_screen_ufo = pygame.image.load("image/deathscene/deathufo.png").convert_alpha()
        death_screen_brick = pygame.image.load("image/deathscene/deathbrick.png").convert_alpha()
        death_screen_helicopter = pygame.image.load("image/deathscene/deathhelicopter.png").convert_alpha()
        ufo_warning_images = load_images("image/UFO_warning")
        ufo_death_light_images = load_images("image/UFO_death_light")

        # Загрузка финального изображения
        try:
            final_screen = pygame.image.load(FINAL_IMAGE_PATH).convert_alpha()
            final_screen = pygame.transform.scale(final_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки финального изображения: {e}")
            # Создаем простой финальный экран если изображение не найдено
            final_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            final_screen.fill((50, 150, 50))
            font = pygame.font.Font(None, 72)
            text = font.render("ПОБЕДА!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            final_screen.blit(text, text_rect)

        # Загрузка кнопки рестарта
        restart_button_img = pygame.Surface((200, 80))
        restart_button_img.fill((100, 100, 100))
        font = pygame.font.Font(None, 36)
        text = font.render("Рестарт", True, (255, 255, 255))
        restart_button_img.blit(text, (restart_button_img.get_width() // 2 - text.get_width() // 2,
                                       restart_button_img.get_height() // 2 - text.get_height() // 2))

        restart_button = ImageButton(
            x=SCREEN_WIDTH - 220,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=80,
            image=restart_button_img,
            hover_image=restart_button_img,
            sound=None
        )

        # Игровые переменные
        char_x = bg_width // 2 - walk_images[0].get_width() // 2
        char_y = LEVEL_MAX_Y - walk_images[0].get_height() - 100
        char_velocity = [0, 0]
        current_frame = 0
        animation_time = 0
        camera_x, camera_y = 0, bg_height - SCREEN_HEIGHT

        # Система врагов с учетом сложности
        eagles = []
        helicopters = []
        ufos = []
        bricks = []
        eagle_spawn_timer = random.uniform(*difficulty_settings['eagle_spawn_range'])
        helicopter_spawn_timer = random.uniform(*difficulty_settings['helicopter_spawn_range'])
        ufo_spawn_timer = random.uniform(*difficulty_settings['ufo_spawn_range'])
        brick_spawn_timer = random.uniform(*difficulty_settings['brick_spawn_range'])

        # Состояние игры
        game_state = STATE_NORMAL
        capture_frame = 0
        darken_alpha = 0
        current_enemy = None
        death_timer = 0
        final_animation_alpha = 0  # Для плавного появления финального экрана

        def spawn_eagle():
            direction = random.choice([-1, 1])
            if direction == 1:
                x = camera_x - 400
            else:
                x = camera_x + SCREEN_WIDTH + 400

            # Новое условие появления - появляемся в видимой области или чуть выше/ниже
            if (camera_y < 14000 and camera_y > 10000):
                # Появляемся в пределах видимой области или рядом
                y = random.randint(int(camera_y - SCREEN_HEIGHT), int(camera_y + SCREEN_HEIGHT))
                # Ограничиваем общим диапазоном уровня
                y = max(LEVEL_MIN_Y, min(y, LEVEL_MAX_Y))
            else:
                # Если камера вне диапазона - появляемся за экраном
                y = 20000

            return {
                'type': 'eagle',
                'x': x,
                'y': y,
                'direction': direction,
                'speed': random.uniform(*difficulty_settings['eagle_speed_range']),
                'frame': 0,
                'active': True
            }

        def spawn_helicopter():
            direction = random.choice([-1, 1])

            # Определяем начальную позицию за пределами экрана
            if direction == 1:
                x = camera_x - 400  # Появляемся слева за границей экрана
            else:
                x = camera_x + SCREEN_WIDTH + 400  # Появляемся справа за границей экрана

            # Используем константы для определения диапазона появления
            min_spawn_y, max_spawn_y = BASE_HELICOPTER_SPAWN_Y_RANGE

            # Определяем вертикальную позицию - либо выше видимой области, либо ниже
            spawn_above = random.choice([True, False])
            if spawn_above:
                y = camera_y - random.randint(200, 500)  # Появляемся выше видимой области
            else:
                y = camera_y + SCREEN_HEIGHT + random.randint(200, 500)  # Появляемся ниже видимой области

            # Ограничиваем общим диапазоном уровня
            y = max(min_spawn_y, min(y, max_spawn_y))

            return {
                'type': 'helicopter',
                'x': x,
                'y': y,
                'direction': direction,
                'speed': random.uniform(*difficulty_settings['helicopter_speed_range']),
                'frame': 0,
                'active': True,
                'state': 'horizontal',
                'state_timer': 0,
                'original_speed': random.uniform(*difficulty_settings['helicopter_speed_range']),
                'vertical_speed': 0,
                'vertical_direction': 0,
                'min_y': min_spawn_y,
                'max_y': max_spawn_y
            }

        def spawn_ufo():
            direction = random.choice([-1, 1])
            if direction == 1:
                x = camera_x - 400
            else:
                x = camera_x + SCREEN_WIDTH + 400

            if (camera_y < 5000 and camera_y > 1000):
                y = random.randint(int(camera_y - SCREEN_HEIGHT), int(camera_y + 600))
            else:
                y = 20000

            return {
                'type': 'ufo',
                'x': x,
                'y': y,
                'direction': direction,
                'speed': random.uniform(*difficulty_settings['ufo_speed_range']) * difficulty_settings[
                    'ufo_chaos_factor'],
                'frame': 0,
                'active': True,
                'state': 'normal',  # normal/warning/death_light/leaving
                'state_timer': 0,
                'laser_active': False,
                'laser_x': 0,
                'laser_y': 0,
                'wave_timer': 0,
                'wave_direction': 1,
                'original_y': y,
                'stop_position': random.choice([600, 850]),
                'has_attacked': False,
                'warning_laser_images': ufo_warning_images,
                'death_laser_images': ufo_death_light_images
            }

        def spawn_brick():
            return {
                'type': 'brick',
                'x': random.choice([822 - 80, 960 + 40]),
                'y': camera_y - 100,
                'speed': random.uniform(*difficulty_settings['brick_speed_range']),
                'frame': 0,
                'active': True
            }

        running = True
        while running:
            dt = clock.tick(FPS) / 1000

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and game_state in [STATE_DEATH, STATE_FINAL]:
                        running = False
                    elif event.key == pygame.K_r and game_state in [STATE_DEATH, STATE_FINAL]:
                        # Рестарт игры по нажатию R
                        return 'restart'
                elif event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_DEATH:
                    # Обработка клика по кнопке рестарта
                    if restart_button.rect.collidepoint(event.pos):
                        return 'restart'

                if game_state == STATE_DEATH:
                    mouse_pos = pygame.mouse.get_pos()
                    restart_button.check_hover(mouse_pos)

                    # Отрисовка кнопки рестарта
                    restart_button.draw(screen)

            # Обновление игры
            if game_state == STATE_NORMAL:
                # Управление персонажем
                keys = pygame.key.get_pressed()
                char_velocity[0] = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * CHAR_SPEED
                char_velocity[1] = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * CHAR_SPEED

                # Движение персонажа
                char_x += char_velocity[0] * dt
                char_y += char_velocity[1] * dt

                # Границы уровня
                char_x = max(LEVEL_MIN_X, min(char_x, LEVEL_MAX_X - walk_images[0].get_width()))
                char_y = max(LEVEL_MIN_Y, min(char_y, LEVEL_MAX_Y - walk_images[0].get_height()))

                # Проверка достижения финала
                if (FINAL_MIN_X <= char_x <= FINAL_MAX_X and char_y <= FINAL_Y):
                    game_state = STATE_FINAL
                    # Можно добавить звук победы здесь

                # Анимация персонажа
                if char_velocity[0] != 0 or char_velocity[1] != 0:
                    animation_time += dt
                    if animation_time >= ANIMATION_SPEED / 100:
                        current_frame = (current_frame + 1) % len(walk_images)
                        animation_time = 0

                # Управление камерой
                char_screen_x = char_x - camera_x
                char_screen_y = char_y - camera_y

                if char_screen_x < CAMERA_LEFT_BORDER:
                    camera_x = char_x - CAMERA_LEFT_BORDER
                elif char_screen_x > CAMERA_RIGHT_BORDER:
                    camera_x = char_x - CAMERA_RIGHT_BORDER

                if char_screen_y < CAMERA_TOP_BORDER:
                    camera_y = char_y - CAMERA_TOP_BORDER
                elif char_screen_y > CAMERA_BOTTOM_BORDER:
                    camera_y = char_y - CAMERA_BOTTOM_BORDER

                camera_x = max(0, min(camera_x, bg_width - SCREEN_WIDTH))
                camera_y = max(0, min(camera_y, bg_height - SCREEN_HEIGHT))

            elif game_state == STATE_FINAL:
                # Плавное появление финального экрана
                final_animation_alpha = min(255, final_animation_alpha + 5)

            # Спавн врагов
            eagle_spawn_timer -= dt
            helicopter_spawn_timer -= dt
            ufo_spawn_timer -= dt
            brick_spawn_timer -= dt

            if eagle_spawn_timer <= 0 and len(eagles) < difficulty_settings['max_eagles']:
                eagles.append(spawn_eagle())
                eagle_spawn_timer = random.uniform(*difficulty_settings['eagle_spawn_range'])

            if helicopter_spawn_timer <= 0 and len(helicopters) < difficulty_settings['max_helicopters']:
                helicopters.append(spawn_helicopter())
                helicopter_spawn_timer = random.uniform(*difficulty_settings['helicopter_spawn_range'])

            if ufo_spawn_timer <= 0 and len(ufos) < difficulty_settings['max_ufos']:
                ufos.append(spawn_ufo())
                ufo_spawn_timer = random.uniform(*difficulty_settings['ufo_spawn_range'])

            if brick_spawn_timer <= 0 and len(bricks) < difficulty_settings['max_bricks']:
                bricks.append(spawn_brick())
                brick_spawn_timer = random.uniform(*difficulty_settings['brick_spawn_range'])

                # Обновление врагов
                for enemy_list in [eagles, helicopters, ufos]:
                    for enemy in enemy_list[:]:
                        enemy['x'] += enemy['speed'] * enemy.get('direction', 1) * dt
                        #enemy['frame'] += 1

                        # Удаление улетевших врагов
                        if ((enemy.get('direction', 1) == 1 and enemy['x'] > camera_x + SCREEN_WIDTH + 400) or
                                (enemy.get('direction', 1) == -1 and enemy['x'] < camera_x - 400)):
                            if enemy == current_enemy and game_state in [STATE_CARRYING, STATE_CAPTURED]:
                                game_state = STATE_DEATH
                                death_timer = 0
                                # Устанавливаем правильный экран смерти в зависимости от типа врага
                                if enemy['type'] == 'ufo':
                                    death_screen = death_screen_ufo
                                elif enemy['type'] == 'eagle':
                                    death_screen = death_screen_birds
                                elif enemy['type'] == 'helicopter':
                                    death_screen = death_screen_helicopter
                            if enemy in enemy_list:
                                enemy_list.remove(enemy)
                            continue

                            # Проверка столкновения
                        if (abs(enemy['x'] - char_x) < 150 and
                                abs(enemy['y'] - char_y) < 150 and
                                game_state == STATE_NORMAL):
                            game_state = STATE_CAPTURED
                            capture_frame = 0
                            current_enemy = enemy
                            # Устанавливаем экран смерти сразу при захвате
                            if enemy['type'] == 'ufo':
                                death_screen = death_screen_ufo
                            elif enemy['type'] == 'eagle':
                                death_screen = death_screen_birds
                            elif enemy['type'] == 'helicopter':
                                death_screen = death_screen_helicopter

            # Обновление орлов
            for eagle in eagles[:]:
                # Плавное движение с учетом времени кадра (dt)
                eagle['x'] += eagle['speed'] * eagle['direction'] * dt
                eagle['y'] += random.uniform(-50, 50) * dt  # Добавляем небольшую вертикальную вариацию

                # Анимация - обновляем кадр каждый цикл, а не раз в несколько секунд
                eagle['frame'] = (eagle['frame'] + 1) % len(eagle_images)

                # Удаление улетевших врагов
                if ((eagle['direction'] == 1 and eagle['x'] > camera_x + SCREEN_WIDTH + 400) or
                        (eagle['direction'] == -1 and eagle['x'] < camera_x - 400)):
                    if eagle == current_enemy and game_state in [STATE_CARRYING, STATE_CAPTURED]:
                        game_state = STATE_DEATH
                        death_timer = 0
                        death_screen = death_screen_birds
                    eagles.remove(eagle)
                    continue

                # Проверка столкновения
                if (abs(eagle['x'] - char_x) < 150 and
                        abs(eagle['y'] - char_y) < 150 and
                        game_state == STATE_NORMAL):
                    game_state = STATE_CAPTURED
                    capture_frame = 0
                    current_enemy = eagle
                    death_screen = death_screen_birds

            for helicopter in helicopters[:]:
                # Удаление улетевших вертолетов (только по горизонтали)
                if ((helicopter['direction'] == 1 and helicopter['x'] > camera_x + SCREEN_WIDTH + 400) or
                        (helicopter['direction'] == -1 and helicopter['x'] < camera_x - 400)):
                    if helicopter == current_enemy and game_state in [STATE_CARRYING, STATE_CAPTURED]:
                        game_state = STATE_DEATH
                        death_screen = death_screen_helicopter
                        death_timer = 0
                    helicopters.remove(helicopter)
                    continue

                # Обновление состояния вертолета
                if helicopter['state'] == 'horizontal':
                    helicopter['x'] += helicopter['speed'] * helicopter['direction'] * dt

                    # Случайный переход в вертикальный режим
                    if random.random() < 0.01:  # 1% шанс каждую итерацию
                        helicopter['state'] = 'vertical'
                        helicopter['state_timer'] = 0
                        helicopter['vertical_direction'] = random.choice([-1, 1])  # Случайное направление
                        helicopter['vertical_speed'] = random.uniform(200, 400) * helicopter['vertical_direction']

                elif helicopter['state'] == 'vertical':
                    helicopter['state_timer'] += dt
                    new_y = helicopter['y'] + helicopter['vertical_speed'] * dt
                    # Ограничиваем движение диапазоном HELICOPTER_SPAWN_Y_RANGE
                    new_y = max(helicopter['min_y'], min(new_y, helicopter['max_y']))
                    helicopter['y'] = new_y
                    # Возврат в горизонтальный режим после 0.5 секунды
                    if helicopter['state_timer'] >= 0.5:
                        helicopter['state'] = 'horizontal'
                        helicopter['speed'] = helicopter['original_speed']

                helicopter['frame'] += 1

                # Проверка столкновения
                if (abs(helicopter['x'] - char_x) < 150 and
                        abs(helicopter['y'] - char_y) < 150 and
                        game_state == STATE_NORMAL):
                    game_state = STATE_CAPTURED
                    capture_frame = 0
                    current_enemy = helicopter
                    death_screen = death_screen_helicopter

            for ufo in ufos[:]:
                if ufo['state'] == 'normal':
                    # Хаотичное движение волной
                    ufo['wave_timer'] += dt
                    if ufo['wave_timer'] >= 1.0:
                        ufo['wave_direction'] *= -1
                        ufo['wave_timer'] = 0

                    wave_offset = 100 * ufo['wave_direction'] * dt * 2
                    ufo['y'] += wave_offset
                    ufo['x'] += ufo['speed'] * ufo['direction'] * dt

                    if ((ufo['direction'] == 1 and ufo['x'] >= ufo['stop_position']) or
                            (ufo['direction'] == -1 and ufo['x'] <= ufo['stop_position'])):
                        ufo['state'] = 'warning'
                        ufo['state_timer'] = 0
                        ufo['speed'] = 0

                elif ufo['state'] == 'warning':
                    ufo['state_timer'] += dt/1.5
                    if ufo['state_timer'] >= difficulty_settings.get('ufo_warning_time', BASE_UFO_WARNING_TIME):
                        ufo['state'] = 'death_light'
                        ufo['state_timer'] = 0
                        ufo['laser_active'] = True
                        ufo['laser_x'] = ufo['x'] + ufo_images[0].get_width() // 2
                        ufo['laser_y'] = ufo['y'] + ufo_images[0].get_height()

                elif ufo['state'] == 'death_light':
                    ufo['state_timer'] += dt
                    if ufo['state_timer'] >= difficulty_settings.get('ufo_death_light_time', BASE_UFO_DEATH_LIGHT_TIME):
                        ufo['state'] = 'leaving'
                        ufo['state_timer'] = 0
                        ufo['laser_active'] = False
                        ufo['speed'] = random.uniform(*difficulty_settings['ufo_speed_range']) * difficulty_settings[
                            'ufo_chaos_factor'] * 1.5
                        ufo['direction'] *= -1
                        ufo['has_attacked'] = True

                elif ufo['state'] == 'leaving':
                    ufo['x'] += ufo['speed'] * ufo['direction'] * dt
                    if ((ufo['direction'] == 1 and ufo['x'] > camera_x + SCREEN_WIDTH + 400) or
                        (ufo['direction'] == -1 and ufo['x'] < camera_x - 400)):
                            ufos.remove(ufo)
                            continue

                ufo['frame'] += 1

                img = (ufo_images_flipped if ufo['direction'] == -1 else ufo_images)[ufo['frame'] % len(ufo_images)]
                screen.blit(img, (ufo['x'] - camera_x, ufo['y'] - camera_y))

                # Отрисовка лазера
                if ufo['laser_active']:
                    if ufo['state'] == 'warning':
                        # Предупредительный лазер (короткий)
                        laser_img = ufo['warning_laser_images'][ufo['frame'] % len(ufo['warning_laser_images'])]
                        screen.blit(laser_img,
                                    (ufo['laser_x'] - laser_img.get_width() // 2 - camera_x,
                                     ufo['laser_y'] - camera_y))
                    elif ufo['state'] == 'death_light':
                        # Смертельный лазер (длинный)
                        laser_img = ufo['death_laser_images'][ufo['frame'] % len(ufo['death_laser_images'])]
                        screen.blit(laser_img,
                                    (ufo['laser_x'] - laser_img.get_width() // 2 - camera_x,
                                     ufo['laser_y'] - camera_y))

                    # Проверка столкновения с лазером
                    if ufo['state'] == 'death_light' and game_state == STATE_NORMAL:
                        laser_img = ufo['death_laser_images'][ufo['frame'] % len(ufo['death_laser_images'])]
                        laser_rect = pygame.Rect(
                            ufo['laser_x'] - LADDER_WIDTH // 2,
                            ufo['laser_y'],
                            LADDER_WIDTH,
                            laser_img.get_height()
                        )
                        char_rect = pygame.Rect(
                            char_x,
                            char_y,
                            walk_images[0].get_width(),
                            walk_images[0].get_height()
                        )

                        if laser_rect.colliderect(char_rect):
                            game_state = STATE_DEATH
                            death_screen = death_screen_ufo  # Явно указываем экран смерти для НЛО
                            death_timer = 0
                            current_enemy = {
                                'type': 'ufo',  # Явно указываем тип врага
                                'object': ufo  # Сохраняем ссылку на сам объект НЛО
                            }
                    if ufo['state'] == 'leaving':
                        ufo['frame'] += 1

            # Обновление кирпичей
            for brick in bricks[:]:
                brick['y'] += brick['speed'] * dt
                brick['frame'] += 1

                # Удаление упавших кирпичей
                if brick['y'] > camera_y + SCREEN_HEIGHT + 100:
                    bricks.remove(brick)
                    continue

                # Проверка столкновения с кирпичом
                if (game_state == STATE_NORMAL and
                        abs(brick['x'] - char_x) < 100 and
                        abs(brick['y'] - char_y) < 100):
                    game_state = STATE_DEATH
                    death_screen = death_screen_brick  # Устанавливаем экран смерти для кирпича
                    death_timer = 0
                    bricks.remove(brick)

            if game_state == STATE_CAPTURED:
                capture_frame += 1
                if capture_frame >= len(capture_images) * 5:
                    game_state = STATE_CARRYING

            elif game_state == STATE_CARRYING:
                if current_enemy:
                    enemy_list = None
                    if current_enemy['type'] == 'eagle':
                        enemy_list = eagles
                    elif current_enemy['type'] == 'helicopter':
                        enemy_list = helicopters
                    elif current_enemy['type'] == 'ufo':
                        enemy_list = ufos

                    if enemy_list and current_enemy in enemy_list:
                        current_enemy['x'] += current_enemy['speed'] * current_enemy.get('direction', 1) * dt
                        char_x = current_enemy['x']
                        char_y = current_enemy['y'] + 100

            elif game_state == STATE_DEATH:
                death_timer += dt
                darken_alpha = min(darken_alpha + 2, 180)
                # Определяем причину смерти
                if current_enemy:
                    if current_enemy['type'] == 'ufo':
                        death_screen = death_screen_ufo
                    elif current_enemy['type'] == 'eagle':
                        death_screen = death_screen_birds
                    elif current_enemy['type'] == 'helicopter':
                        death_screen = death_screen_helicopter
                    else:  # Для кирпичей и других случаев
                        death_screen = death_screen_brick
                else:
                    death_screen = death_screen_brick  # По умолчанию для других случаев
                if death_timer > 3:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        running = False

            # Отрисовка
            screen.fill((0, 0, 0))

            if game_state != STATE_FINAL:
                # Отрисовка игрового мира
                screen.blit(background, (0, 0), area=(camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT))

                # Персонаж
                if game_state == STATE_NORMAL:
                    screen.blit(walk_images[current_frame], (char_x - camera_x, char_y - camera_y))
                elif game_state in [STATE_CAPTURED, STATE_CARRYING]:
                    img_idx = min(capture_frame // 5, len(capture_images) - 1)
                    screen.blit(capture_images[img_idx], (char_x - camera_x, char_y - camera_y))

            # Враги
            for eagle in eagles:
                img = (eagle_images_flipped if eagle['direction'] == -1 else eagle_images)[
                    eagle['frame'] % len(eagle_images)]
                screen.blit(img, (eagle['x'] - camera_x, eagle['y'] - camera_y))

            for helicopter in helicopters:
                img = (helicopter_images_flipped if helicopter['direction'] == -1 else helicopter_images)[
                    helicopter['frame'] % len(helicopter_images)]
                screen.blit(img, (helicopter['x'] - camera_x, helicopter['y'] - camera_y))

            for ufo in ufos:
                if ufo['state'] == 'normal':
                    img = (ufo_images_flipped if ufo['direction'] == -1 else ufo_images)[ufo['frame'] % len(ufo_images)]
                elif ufo['state'] == 'warning':
                    img = ufo_warning_images[ufo['frame'] % len(ufo_warning_images)]
                elif ufo['state'] == 'death_light':
                    img = ufo_death_light_images[ufo['frame'] % len(ufo_death_light_images)]
                elif ufo['state'] == 'leaving':
                    img = (ufo_images_flipped if ufo['direction'] == -1 else ufo_images)[ufo['frame'] % len(ufo_images)]

                screen.blit(img, (ufo['x'] - camera_x, ufo['y'] - camera_y))

                # Отрисовка лазера (полупрозрачного)
                if ufo['laser_active']:
                    laser_surface = pygame.Surface((BASE_UFO_LASER_WIDTH, BASE_UFO_LASER_LENGTH), pygame.SRCALPHA)
                    laser_surface.fill((255, 0, 0, 128))  # Красный полупрозрачный
                    screen.blit(laser_surface,
                                (ufo['laser_x'] - BASE_UFO_LASER_WIDTH // 2 - camera_x, ufo['laser_y'] - camera_y))

            # Кирпичи
            for brick in bricks:
                img = brick_images[brick['frame'] % len(brick_images)]
                screen.blit(img, (brick['x'] - camera_x, brick['y'] - camera_y))
            else:
                # Отрисовка финального экрана
                final_screen.set_alpha(final_animation_alpha)
                screen.blit(final_screen, (0, 0))

                # Дополнительный текст
                if final_animation_alpha == 255:
                    font = pygame.font.Font(None, 36)
                    text = font.render("Нажмите ESC для выхода или R для рестарта", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                    screen.blit(text, text_rect)

            # Экран смерти
            if game_state == STATE_DEATH:
                dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                dark_surface.set_alpha(darken_alpha)
                dark_surface.fill((0, 0, 0))
                screen.blit(dark_surface, (0, 0))
                screen.blit(death_screen, (
                    SCREEN_WIDTH // 2 - death_screen.get_width() // 2,
                    SCREEN_HEIGHT // 2 - death_screen.get_height() // 2
                ))

                # Обновляем и рисуем кнопку рестарта
                mouse_pos = pygame.mouse.get_pos()
                restart_button.check_hover(mouse_pos)
                restart_button.draw(screen)

                # Отображаем подсказку про клавишу R
                font = pygame.font.Font(None, 36)
                text = font.render("Нажмите R или кнопку для рестарта", True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
                screen.blit(text, text_rect)

            pygame.display.flip()

    except Exception as e:
        print(f"Ошибка в main_game: {e}")
        pygame.quit()
        sys.exit(1)

