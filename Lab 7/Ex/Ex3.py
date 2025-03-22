import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
screen.fill((255, 255, 255))

isDone = True
mainCoordX, mainCoordY = 250, 250

while isDone:
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, 'Red', (mainCoordX, mainCoordY), 25)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and mainCoordY - 45 >= 0:
                mainCoordY -= 20
            if event.key == pygame.K_DOWN and mainCoordY + 45 <= 500:
                mainCoordY += 20
            if event.key == pygame.K_RIGHT and mainCoordX + 45 <= 500:
                mainCoordX += 20
            if event.key == pygame.K_LEFT and mainCoordX - 45 >= 0:
                mainCoordX -= 20
