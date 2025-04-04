import pygame
import sys

pygame.init()  # Инициализация библиотеки Pygame

# Экран и цвета
screen = pygame.display.set_mode((800, 600))  # Устанавливаем размеры экрана 800x600 пикселей
pygame.display.set_caption("paint")  # Название окна
WHITE = (255, 255, 255)  # Белый цвет
BLACK = (0, 0, 0)  # Черный цвет
RED = (255, 0, 0)  # Красный цвет
GREEN = (0, 255, 0)  # Зеленый цвет
BLUE = (0, 0, 255)  # Синий цвет
current_color = BLACK  # Изначальный цвет кисти - черный

screen.fill(WHITE)  # Заполняем экран белым цветом

# Настройки кисти и режимов рисования
brush_size = 5  # Размер кисти
drawing = False  # Флаг для проверки, рисуем ли мы сейчас
last_pos = None  # Последняя позиция мыши, используем для рисования линии
mode = "brush"  # Режим рисования, изначально кисть
start_pos = None  # Начальная позиция для рисования

# Главный игровой цикл
while True:
    for event in pygame.event.get():  # Обрабатываем все события
        if event.type == pygame.QUIT:  # Если нажата кнопка выхода (крестик в углу окна)
            pygame.quit()  # Закрываем Pygame
            sys.exit()  # Завершаем программу

        # Обработка нажатий клавиш для изменения режима рисования или цвета
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Если нажата клавиша R, меняем цвет на красный
                current_color = RED
            elif event.key == pygame.K_g:  # Если нажата клавиша G, меняем цвет на зеленый
                current_color = GREEN
            elif event.key == pygame.K_b:  # Если нажата клавиша B, меняем цвет на синий
                current_color = BLUE
            elif event.key == pygame.K_e:  # Если нажата клавиша E, переключаем на режим ластика
                mode = "eraser"
            elif event.key == pygame.K_t:  # Если нажата клавиша T, переключаем на режим кисти
                mode = "brush"
            elif event.key == pygame.K_c:  # Если нажата клавиша C, переключаем на режим рисования круга
                mode = "circle"
            elif event.key == pygame.K_q:  # Если нажата клавиша Q, переключаем на режим рисования квадрата
                mode = "square"
            elif event.key == pygame.K_p:  # Если нажата клавиша P, переключаем на режим рисования прямоугольного треугольника
                mode = "right_triangle"
            elif event.key == pygame.K_d:  # Если нажата клавиша D, переключаем на режим рисования ромба
                mode = "rhombus"
            elif event.key == pygame.K_l:  # Если нажата клавиша L, переключаем на режим рисования прямоугольника
                mode = "rect"

        # Если нажата кнопка мыши (начало рисования)
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True  # Начинаем рисовать
            start_pos = event.pos  # Сохраняем начальную точку рисования
            last_pos = event.pos  # Сохраняем последнюю точку

        # Если кнопка мыши отпущена (конец рисования)
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos  # Сохраняем конечную точку рисования

            # Рисуем прямоугольник
            if mode == "rect":  
                rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                   abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                pygame.draw.rect(screen, current_color, rect, width=2)  # Рисуем прямоугольник

            # Рисуем круг
            elif mode == "circle":  
                radius = int(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, width=2)  # Рисуем круг

            # Рисуем квадрат
            elif mode == "square":  
                side = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))  # Сторона квадрата
                rect = pygame.Rect(start_pos[0], start_pos[1], side, side)  # Создаем прямоугольник с одинаковыми сторонами
                pygame.draw.rect(screen, current_color, rect, width=2)  # Рисуем квадрат

            # Рисуем прямоугольный треугольник
            elif mode == "right_triangle":  
                x1, y1 = start_pos
                x2, y2 = end_pos
                points = [start_pos, (x1, y2), (x2, y2)]  # Определяем вершины треугольника
                pygame.draw.polygon(screen, current_color, points, width=2)  # Рисуем треугольник

            # Рисуем равносторонний треугольник
            elif mode == "equilateral_triangle":  
                x1, y1 = start_pos
                x2, y2 = end_pos
                side = max(abs(x2 - x1), abs(y2 - y1))
                point1 = (x1, y1)
                point2 = (x1 + side, y1)
                point3 = (x1 + side / 2, y1 - (3**0.5/2)*side)  # Вычисляем высоту для равностороннего треугольника
                pygame.draw.polygon(screen, current_color, [point1, point2, point3], width=2)  # Рисуем треугольник

            # Рисуем ромб
            elif mode == "rhombus":  
                x1, y1 = start_pos
                x2, y2 = end_pos
                center_x = (x1 + x2) // 2  # Определяем центр ромба
                center_y = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2  # Половина ширины ромба
                dy = abs(y2 - y1) // 2  # Половина высоты ромба
                points = [
                    (center_x, center_y - dy),  # Верхний угол
                    (center_x + dx, center_y),  # Правый угол
                    (center_x, center_y + dy),  # Нижний угол
                    (center_x - dx, center_y)   # Левый угол
                ]
                pygame.draw.polygon(screen, current_color, points, width=2)  # Рисуем ромб

            drawing = False  # Заканчиваем рисование

        # Рисование во время движения мыши (только для кисти и ластика)
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":  # Режим кисти
                pygame.draw.line(screen, current_color, last_pos, event.pos, brush_size)  # Рисуем линию
                last_pos = event.pos  # Обновляем последнюю позицию

            elif mode == "eraser":  # Режим ластика
                pygame.draw.line(screen, WHITE, last_pos, event.pos, brush_size * 2)  # Рисуем линию белого цвета (стирать)
                last_pos = event.pos  # Обновляем последнюю позицию

    pygame.display.update()  # Обновляем экран



# Клавиши и их функции:
# R – Выбор красного цвета
# G – Выбор зеленого цвета
# B – Выбор синего цвета
# E – Режим ластика (стереть рисунок)
# T – Режим кисти (рисовать)
# C – Режим рисования круга
# Q – Режим рисования прямоугольника
# P – Режим рисования прямоугольного треугольника
# E – Режим рисования равнобедренного треугольника
# D – Режим рисования ромба
# L – Режим рисования прямоугольника
