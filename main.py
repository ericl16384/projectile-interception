import pygame

import interception

pygame.init()

# Set the height and width of the screen
size = [1500, 750]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("main.py")


interception.objects.extend([
    interception.Shooter((200, 200)),
    interception.Target((1000, 400), (-2, 0))
])


done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill("black")

    for o in interception.objects:
        o.draw(screen)

    pygame.display.flip()


    i = 0
    while i < len(interception.objects):
        o = interception.objects[i]
        o.update()
        if not o.valid:
            interception.objects.pop(i)
            continue
        i += 1


pygame.quit()