import pygame
from pygame.locals import *
import random 
import time

pygame.init()  # Инициализация всех модулей pygame

# Настройки игры
FPS = 120  # Частота кадров
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Начальная скорость движения объектов
SCORE = 0  # Очки за уклонение от врагов
COINS_COLLECTED = 0  # Количество собранных монет

# Звук монеты
coin_sound = pygame.mixer.Sound("Lab 8/sounds/звук монеты.mp3")

# Шрифты и надписи
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Times New Roman", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

# Загрузка фонового изображения
background = pygame.image.load("Lab 8/images/street.png")

# Фоновая музыка
pygame.mixer.music.load("Lab 8/sounds/Lectures_Lecture8_racer_resources_background.wav")
pygame.mixer.music.play(-1)  # Воспроизводится бесконечно

# Основное игровое окно
DISPLAY = pygame.display.set_mode((400, 600))
DISPLAY.fill((255, 255, 255))  # Фон белый
pygame.display.set_caption("GAME")  # Название окна

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Lab 8/images/enemy.png")  # Изображение врага
        self.image = pygame.transform.scale(self.image, (50, 100))  # Масштабирование
        self.rect = self.image.get_rect()  # Прямоугольная область спрайта
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)  # Случайная позиция по горизонтали

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Движение вниз
        if self.rect.bottom > 600:  # Если вышел за нижний край
            SCORE += 1  # Добавляем очко
            self.rect.top = 0  # Возвращаем наверх
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)  # Новая позиция

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Lab 8/images/player.png")  # Изображение игрока
        self.image = pygame.transform.scale(self.image, (50, 100))  # Масштабирование
        self.rect = self.image.get_rect()
        self.rect.center = (207, 520)  # Стартовая позиция

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Получаем нажатые клавиши
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)  # Движение влево
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)  # Движение вправо

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("Lab 8/images/photo_2025-04-04_14-15-14.jpg")  # Монета
        self.image = pygame.transform.scale(self.original_image, (40, 40))  # Размер
        self.rect = self.image.get_rect()
        self.respawn()  # Начальное появление

    def respawn(self):
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)  # Новая позиция сверху

    def move(self):
        self.rect.move_ip(0, SPEED // 2)  # Движение вниз медленнее врагов
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()  # Если пропущена — снова сверху

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Каждую секунду

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3  # Постепенное увеличение скорости
        if event.type == QUIT:
            pygame.quit()  # Выход из игры

    DISPLAY.blit(background, (0, 0))  # Отображение фона

    # Отображение счета и монет
    scores = font_small.render(str(SCORE), True, (0, 0, 0))
    DISPLAY.blit(scores, (10, 10))
    coins_collected_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, (0, 0, 0))
    DISPLAY.blit(coins_collected_text, (300, 10))

    # Движение и отрисовка всех объектов
    for entity in all_sprites:
        if isinstance(entity, Enemy) or isinstance(entity, Player) or isinstance(entity, Coin):
            entity.move()
        DISPLAY.blit(entity.image, entity.rect)

    # Столкновение с врагом — конец игры
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.Sound("Lab 8/sounds/Lectures_Lecture8_racer_resources_crash.wav").play()
        time.sleep(0.7)
        DISPLAY.fill((255, 0, 0))  # Красный экран
        DISPLAY.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Удаление всех объектов
        time.sleep(1)
        pygame.quit()

    # Столкновение с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1  # Увеличиваем счетчик
        coin_sound.play()  # Воспроизводим звук
        C1.respawn()  # Появляется новая монета

    pygame.display.update()  # Обновление экрана
    FramePerSec.tick(FPS)  # Поддержание FPS
