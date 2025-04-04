import pygame
import sys

pygame.init()  # Инициализация Pygame

# Параметры экрана
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20  # Не используется, но может пригодиться для сетки
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
current_color = BLACK  # Текущий цвет кисти

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")  # Название окна
font = pygame.font.SysFont("Times New Roman", 20)
screen.fill(WHITE)  # Белый фон

# Параметры кнопок цветов
button_width = 50
button_height = 50

brush_size = 5  # Размер кисти
drawing = False  # Флаг рисования
last_pos = None  # Последняя позиция мыши
mode = "brush"  # Режим: по умолчанию кисть
start_pos = None  # Начальная точка фигуры (круг/прямоугольник)

# Координаты кнопок выбора цвета
color_buttons = {
    'red': (10, 10),
    'green': (70, 10),
    'blue': (130, 10),
    'black': (190, 10),
}

# Функция отрисовки цветных кнопок
def draw_color_buttons():
    pygame.draw.rect(screen, RED, (color_buttons['red'][0], color_buttons['red'][1], button_width, button_height))
    pygame.draw.rect(screen, GREEN, (color_buttons['green'][0], color_buttons['green'][1], button_width, button_height))
    pygame.draw.rect(screen, BLUE, (color_buttons['blue'][0], color_buttons['blue'][1], button_width, button_height))
    pygame.draw.rect(screen, BLACK, (color_buttons['black'][0], color_buttons['black'][1], button_width, button_height))

# Главный цикл приложения
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Переключение режимов рисования по клавишам
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                mode = "eraser"  # Ластик
            elif event.key == pygame.K_t:
                mode = "brush"  # Кисть
            elif event.key == pygame.K_c:
                mode = "circle"  # Круг
            elif event.key == pygame.K_r:
                mode = "rect"  # Прямоугольник

        # Обработка нажатия мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos  # Начало фигуры
            last_pos = event.pos  # Последняя точка для кисти

            # Проверка нажатий по кнопкам цветов
            if color_buttons['red'][0] < event.pos[0] < color_buttons['red'][0] + button_width and \
                    color_buttons['red'][1] < event.pos[1] < color_buttons['red'][1] + button_height:
                current_color = RED
            elif color_buttons['green'][0] < event.pos[0] < color_buttons['green'][0] + button_width and \
                    color_buttons['green'][1] < event.pos[1] < color_buttons['green'][1] + button_height:
                current_color = GREEN
            elif color_buttons['blue'][0] < event.pos[0] < color_buttons['blue'][0] + button_width and \
                    color_buttons['blue'][1] < event.pos[1] < color_buttons['blue'][1] + button_height:
                current_color = BLUE
            elif color_buttons['black'][0] < event.pos[0] < color_buttons['black'][0] + button_width and \
                    color_buttons['black'][1] < event.pos[1] < color_buttons['black'][1] + button_height:
                current_color = BLACK

        # Отпускание мыши — отрисовка фигур
        if event.type == pygame.MOUSEBUTTONUP:
            if mode == "rect":
                end_pos = event.pos
                # Создание прямоугольника от start_pos до end_pos
                rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                   abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                pygame.draw.rect(screen, current_color, rect, width=2)  # Контур прямоугольника
            elif mode == "circle":
                end_pos = event.pos
                # Вычисление радиуса круга по расстоянию
                radius = int(((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, width=2)  # Контур круга

            drawing = False  # Заканчиваем рисовать

        # Движение мыши — рисуем кистью или стираем
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.line(screen, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos  # Обновляем последнюю позицию
            elif mode == "eraser":
                pygame.draw.line(screen, WHITE, last_pos, event.pos, brush_size * 2)
                last_pos = event.pos

    draw_color_buttons()  # Обновление кнопок цветов
    pygame.display.update()  # Обновление экрана
