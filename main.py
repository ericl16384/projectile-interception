import pygame, random

import interception

pygame.init()

# Set the height and width of the screen
size = [1500, 750]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("main.py")


interception.objects.extend([
    interception.Shooter((500, 375), (0, 0)),
    interception.Shooter((1000, 375), (0, 0)),
    
    # interception.Target((200, 400), (0.5, 0)),
    # interception.Target((200, 300), (1, 0)),
    # interception.Target((200, 500), (0.5, 0)),
    # # interception.Target((1500, 200), (-2, 0)),
    # # interception.Target((1500, 300), (-2, 0))
])

for i in range(10):
    # interception.objects.append(interception.Target((100, 125 + i*100), (0, 0)))
    interception.add_target()


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