from player import player
from bird import birds
from config import crane


# Функция для проверки столкновений
def check_collision():
    for bird in birds:
        if player.colliderect(bird["rect"]):
            return bird["direction"], bird["rect"].center  # Возвращаем направление птицы и её центр
    return None, None

# Проверка достижения крана
def check_reach_crane():
    return player.colliderect(crane)