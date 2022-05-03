import pygame, sys, main, pugixor
rreg = pugixor.XorDocumentRead("rreg.xor")
import gui

pygame.init()

FPS = 120
SCREEN_WIDTH = 800#pygame.display.Info().current_w
SCREEN_HEIGHT = 600#pygame.display.Info().current_h
BG_COLOR = pygame.Color("#2B2B2B")
version = 0.1

sc = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
clock = pygame.time.Clock()

mouse_pressed = 0
up_key = 0
down_key = 1
theme_change = 0
timer = 0

windows = pygame.sprite.Group()
# base = gui.UserPicMan(100, 100)
# windows.add(base)

links = pygame.sprite.Group()

panel = pygame.sprite.Group()
panel.add(gui.Panel())

exec(open("scripts/links.py", encoding="UTF-8").read())

exec(open("scripts/autorun.py", encoding="UTF-8").read())

while True:
    events = pygame.event.get()
    mouse_pressed = 0
    up_key = 0
    down_key = 0
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            up_key = 1
            print(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            down_key = 1

    sc.fill(BG_COLOR)

    try:
        for link in links.spritedict:
            link.update(sc)
    except RuntimeError:
        pass

    try:
        for window in windows.spritedict:
            if not window.close:
                window.update()
                sc.blit(window.image, window.rect)
            else:
                windows.remove(window)
    except RuntimeError:
        pass

    try:
        for window in panel.spritedict:
            window.update()
            sc.blit(window.image, window.rect)
    except RuntimeError:
        pass

    if timer >= 1:
        timer = 0
        main.theme_change = 0
    if theme_change:
        timer += 1

    pygame.display.flip()