import pygame
import random
import sys

pygame.init()  # Инициализация Pygame

# Размеры экрана и клетки
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")  # Название окна
font = pygame.font.SysFont("Times New Roman", 20)
clock = pygame.time.Clock()  # Таймер для контроля FPS

# Начальное состояние змейки
snake = [(100, 100), (80, 100), (60, 100)]  # Координаты сегментов змейки
snake_dir = (20, 0)  # Направление движения (вправо)
food_pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))  # Еда в случайной клетке
score = 0  # Очки
level = 1  # Уровень сложности
speed = 10  # Начальная скорость

# Функция генерации новой еды
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:  # Убедимся, что еда не появляется на змейке
            return (x, y)

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Закрытие окна
            pygame.quit()
            sys.exit()

    # Управление змейкой с клавиатуры
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, 20):
        snake_dir = (0, -20)
    if keys[pygame.K_DOWN] and snake_dir != (0, -20):
        snake_dir = (0, 20)
    if keys[pygame.K_LEFT] and snake_dir != (20, 0):
        snake_dir = (-20, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-20, 0):
        snake_dir = (20, 0)

    # Новая голова змейки
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # Проверка на столкновение со стенами
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        break  # Игра окончена

    # Проверка на столкновение с самой собой
    if new_head in snake:
        break  # Игра окончена

    snake.insert(0, new_head)  # Добавляем новую голову змейки

    # Проверка съела ли змейка еду
    if new_head == food_pos:
        score += 1  # Увеличиваем счет
        food_pos = generate_food()  # Генерируем новую еду
        if score % 4 == 0:  # Каждые 4 очка повышаем уровень
            level += 1
            speed += 2  # И увеличиваем скорость
    else:
        snake.pop()  # Удаляем последний сегмент, если еду не съели

    screen.fill(WHITE)  # Очищаем экран

    # Отрисовка змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Отрисовка еды
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # Отображение счета и уровня
    score_text = font.render(f"Счет: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()  # Обновление экрана
    clock.tick(speed)  # Контроль скорости игры
