import pygame
import random
import sys
import time

pygame.init()  # Инициализация Pygame

WIDTH, HEIGHT = 600, 600  # Размеры экрана
CELL_SIZE = 20  # Размер каждой клетки змейки
WHITE = (255, 255, 255)  # Цвет фона (белый)
GREEN = (0, 255, 0)  # Цвет змейки (зеленый)
BLACK = (0, 0, 0)  # Цвет текста (черный)
FPS = 10  # Частота кадров в секунду

# Словарь для хранения цветов пищи в зависимости от её веса
FOOD_COLORS = {
    1: (255, 0, 0),  # Красный цвет для пищи весом 1
    2: (255, 165, 0),  # Оранжевый цвет для пищи весом 2
    3: (255, 255, 0)  # Желтый цвет для пищи весом 3
}

# Создаем экран для игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")  # Заголовок окна
font = pygame.font.SysFont("Times New Roman", 20)  # Шрифт для текста
clock = pygame.time.Clock()  # Объект для контроля скорости игры

# Начальная позиция змейки (список с координатами сегментов змейки)
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (20, 0)  # Начальное направление змейки (вправо)

# Начальные данные для пищи
food_pos = None  # Начальная позиция пищи
food_weight = 1  # Начальный вес пищи (1)
food_spawn_time = 0  # Время появления пищи

# Игровые переменные
score = 0  # Очки
level = 1  # Уровень
speed = 10  # Скорость игры

# Функция для генерации случайной пищи
def generate_food():
    while True:  # Бесконечный цикл до тех пор, пока не будет найдена подходящая позиция для пищи
        x = random.randrange(0, WIDTH, CELL_SIZE)  # Случайная координата X
        y = random.randrange(0, HEIGHT, CELL_SIZE)  # Случайная координата Y
        if (x, y) not in snake:  # Проверка, чтобы пища не оказалась на змейке
            return (x, y), random.choice([1, 2, 3])  # Возвращаем позицию пищи и случайный вес (1, 2 или 3)

food_pos, food_weight = generate_food()  # Генерируем первую пищу
food_spawn_time = time.time()  # Записываем время появления пищи

while True:  # Главный игровой цикл
    for event in pygame.event.get():  # Обрабатываем все события
        if event.type == pygame.QUIT:  # Если пользователь закрывает окно
            pygame.quit()  # Закрываем Pygame
            sys.exit()  # Завершаем программу

    # Обработка движения змейки
    keys = pygame.key.get_pressed()  # Получаем нажатые клавиши
    if keys[pygame.K_UP] and snake_dir != (0, 20):  # Если нажата стрелка вверх, и змейка не двигается вниз
        snake_dir = (0, -20)  # Меняем направление на вверх
    if keys[pygame.K_DOWN] and snake_dir != (0, -20):  # Если нажата стрелка вниз, и змейка не двигается вверх
        snake_dir = (0, 20)  # Меняем направление на вниз
    if keys[pygame.K_LEFT] and snake_dir != (20, 0):  # Если нажата стрелка влево, и змейка не двигается вправо
        snake_dir = (-20, 0)  # Меняем направление на влево
    if keys[pygame.K_RIGHT] and snake_dir != (-20, 0):  # Если нажата стрелка вправо, и змейка не двигается влево
        snake_dir = (20, 0)  # Меняем направление на вправо

    # Вычисляем новую позицию головы змейки
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # Проверка на столкновение с границами экрана или с самой собой
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake  # Если змейка врезалась в себя
    ):
        break  # Останавливаем игру

    snake.insert(0, new_head)  # Добавляем новую голову в начало списка

    # Если змейка съела пищу
    if new_head == food_pos:
        score += food_weight  # Добавляем очки в зависимости от веса пищи
        food_pos, food_weight = generate_food()  # Генерируем новую пищу
        food_spawn_time = time.time()  # Обновляем время появления пищи
        if score // 4 + 1 > level:  # Если игрок набрал достаточно очков для повышения уровня
            level += 1  # Увеличиваем уровень
            speed += 2  # Увеличиваем скорость игры
    else:
        snake.pop()  # Убираем последний сегмент змейки (движемся вперед)

    # Если с момента появления пищи прошло больше 5 секунд, генерируем новую пищу
    if time.time() - food_spawn_time >= 5:
        food_pos, food_weight = generate_food()
        food_spawn_time = time.time()

    screen.fill(WHITE)  # Очищаем экран (рисуем фон)

    # Рисуем каждый сегмент змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Рисуем пищу с учетом ее веса (цвет зависит от веса)
    food_color = FOOD_COLORS[food_weight]
    pygame.draw.rect(screen, food_color, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # Рисуем счет и уровень
    score_text = font.render(f"Счет: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()  # Обновляем экран
    clock.tick(speed)  # Контролируем скорость игры (частота кадров)
