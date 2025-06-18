import sys
from config import *
from load_screen import load_resources
from main_menu import main_menu
from main_game import main_game

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крановщик")
clock = pygame.time.Clock()


def main():
    """Главная функция программы"""
    try:
        print("Запуск игры...")  # Отладочное сообщение

        # Инициализация Pygame
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        icon = pygame.image.load('image/system/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Крановщик")
        clock = pygame.time.Clock()

        # Загрузка ресурсов
        print("Загрузка ресурсов...")  # Отладочное сообщение
        resources = load_resources()

        # Главный игровой цикл
        while True:
            # Запуск главного меню
            print("Переход в главное меню...")  # Отладочное сообщение
            result = main_menu(resources)
            print(f"Результат из меню: {result}")  # Отладочное сообщение

            if result and len(result) == 2:
                action, difficulty = result
                if action == 'game':
                    print("Запуск основной игры...")  # Отладочное сообщение
                    game_result = main_game(difficulty)
                    if game_result == 'restart':
                        continue  # Начинаем игру заново
                    if game_result == 'restart':
                        continue  # Начинаем игру заново

    except Exception as e:
        print(f"Произошла критическая ошибка: {e}")  # Отладочное сообщение
        import traceback
        traceback.print_exc()  # Печать полного стека ошибки
    finally:
        print("Завершение работы игры...")  # Отладочное сообщение
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()