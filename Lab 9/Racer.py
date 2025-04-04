import pygame
from pygame.locals import *
import random
import time

pygame.init()  # Инициализация Pygame

FPS = 120  # Частота кадров
FramePerSec = pygame.time.Clock()

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5  # Начальная скорость врагов и монет
SCORE = 0  # Очки (считается по пройденным врагам)
COINS_COLLECTED = 0  # Количество собранных монет
PREV_MILESTONE = 0  # Предыдущий порог для увеличения скорости от монет

# Звук монеты
coin_sound = pygame.mixer.Sound("Lab 8/sounds/звук монеты.mp3")

# Создание окна
DISPLAY = pygame.display.set_mode((400, 600))
DISPLAY.fill((255, 255, 255))  # Белый фон
pygame.display.set_caption("GAME")

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Times New Roman", 20)

# Текст "Game Over"
game_over = font.render("Game Over", True, (0, 0, 0))

# Фоновое изображение
background = pygame.image.load("Lab 8/images/street.png")

# Фоновая музыка
pygame.mixer.music.load("Lab 8/sounds/Lectures_Lecture8_racer_resources_background.wav")
pygame.mixer.music.play(-1)  # Бесконечный цикл воспроизведения

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Lab 8/images/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Двигаем вниз
        if self.rect.bottom > 600:  # Если вышел за экран
            SCORE += 1  # Увеличиваем счет
            self.rect.top = 0  # Перезапуск сверху
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Lab 8/images/player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (207, 520)  # Начальная позиция

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)  # Влево
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)  # Вправо

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.respawn()  # Сразу вызываем метод респавна

    def respawn(self):
        weights = [1, 2, 3]  # Вес каждой монеты
        self.weight = random.choice(weights)
        image_path = f"lab8\Racer\images\coin{self.weight}.jpg"  # Не используется, можно удалить
        self.original_image = pygame.image.load("Lab 8/images/coin1.png")
        size = 30 + self.weight * 5  # Размер зависит от веса
        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        self.rect.move_ip(0, SPEED // 2)  # Медленнее врага
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()  # Перерисовать сверху

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

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3  # Постепенное ускорение
        if event.type == QUIT:
            pygame.quit()

    # Отрисовка фона
    DISPLAY.blit(background, (0, 0))

    # Отображение счета и монет
    scores = font_small.render(str(SCORE), True, (0, 0, 0))
    DISPLAY.blit(scores, (10, 10))
    coins_collected_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, (0, 0, 0))
    DISPLAY.blit(coins_collected_text, (300, 10))

    # Движение и отрисовка всех объектов
    for entity in all_sprites:
        entity.move()
        DISPLAY.blit(entity.image, entity.rect)

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()  # Остановить музыку
        pygame.mixer.Sound("Lab 8/sounds/Lectures_Lecture8_racer_resources_crash.wav").play()  # Звук столкновения
        time.sleep(0.7)
        DISPLAY.fill((255, 0, 0))  # Красный экран
        DISPLAY.blit(game_over, (30, 250))  # Текст Game Over
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Удаление всех объектов
        time.sleep(1)
        pygame.quit()  # Закрыть игру

    # Столкновение с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += C1.weight  # Увеличить счет монет
        coin_sound.play()  # Звук монеты
        C1.respawn()  # Новая монета
        if COINS_COLLECTED // 10 > PREV_MILESTONE:
            SPEED += 0.5  # Дополнительное ускорение за каждые 10 монет
            PREV_MILESTONE = COINS_COLLECTED // 10

    pygame.display.update()  # Обновление экрана
    FramePerSec.tick(FPS)  # Ограничение FPS
