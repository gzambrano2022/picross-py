import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
x = 300
y = 300
running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y -= 10
            elif event.key == pygame.K_s:
                y += 10
            elif event.key == pygame.K_a:
                x -= 10
            elif event.key == pygame.K_d:
                x += 10
    window.fill((0, 0, 0))
    pygame.draw.rect(window, 'red', (x,y,300,240))
    pygame.display.update()

pygame.quit()