import pygame
import os

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

MUSIC_FOLDER = r"/Users/bekzatamantay/PP2/Lab 7/Sounds"

if not os.path.exists(MUSIC_FOLDER):
    exit()

sounds = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

if not sounds:
    exit()

index = 0  
isPaused = False

pygame.font.init()
font = pygame.font.Font(None, 36)

def draw_button(text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, gray, rect, border_radius=5)
    text_surface = font.render(text, True, black)
    screen.blit(text_surface, (x + 10, y + 10))
    return rect

def play_music():
    global isPaused
    pygame.mixer.music.load(sounds[index])
    pygame.mixer.music.play()
    isPaused = False

running = True
while running:
    screen.fill(black)
    
    play_btn = draw_button("Play", 50, 400, 100, 50)
    pause_btn = draw_button("Pause", 200, 400, 100, 50)
    next_btn = draw_button("Next", 350, 400, 100, 50)
    prev_btn = draw_button("Previous", 50, 300, 150, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.collidepoint(event.pos):
                play_music()
            elif pause_btn.collidepoint(event.pos):
                pygame.mixer.music.pause()
                isPaused = True
            elif next_btn.collidepoint(event.pos):
                index = (index + 1) % len(sounds)
                play_music()
            elif prev_btn.collidepoint(event.pos):
                index = (index - 1) % len(sounds)
                play_music()
    
    pygame.display.flip()

pygame.quit()
