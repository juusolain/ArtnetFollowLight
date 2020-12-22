import configparser
from fixture import Fixture
from typing import List
import lights
import asyncio
import threading
import pygame
from pygame import gfxdraw
import questionary

config = configparser.ConfigParser()
config.read('config.ini')

stage_min_x = config['display'].getfloat('stage_min_x')
stage_max_x = config['display'].getfloat('stage_max_x')
stage_min_y = config['display'].getfloat('stage_min_y')
stage_max_y = config['display'].getfloat('stage_max_y')

stage_width = stage_max_x - stage_min_x
stage_height = stage_max_y - stage_min_y

framerate = config['display'].getint('framerate')

speed = config['control'].getfloat('speed')

scale = config['display'].getint('scale')
size = width, height = int(stage_width*scale), int(stage_height*scale)

pygame.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont('Calibri', 20)
pause_text = font.render('Output paused', False, (200, 200, 200))

screen = pygame.display.set_mode(size)

running = True

def coordinate_translate(x: float, y: float) -> (int, int):
    x = x/stage_width
    y = y/stage_height

    y = 1 - y

    x = int(x*size[0] + size[0]/2)
    y = int(y*size[1] - size[1]/2)

    return (x, y)

def update():
    screen.fill((10,10,10))
    tx, ty = coordinate_translate(lights.current_target['x'], lights.current_target['y'])
    aa_circle(screen, tx, ty, 2*scale, (255,150,150))
    pygame.draw.circle(surface=screen, radius=2*scale, center=(tx, ty), color=(255,150,150))
    for f in lights.fixtures:
        x, y = coordinate_translate(f.x, f.y)
        pygame.draw.aaline(screen, (50,100,50), (x, y), (tx, ty))
        aa_circle(screen, x, y, scale, (150,255,150))

    if lights.paused:
        screen.blit(pause_text,(20,20))

    pygame.display.flip()

def aa_circle(surf, x, y, radius, color):
    gfxdraw.aacircle(surf, x, y, radius, color)
    gfxdraw.filled_circle(surf, x, y, radius, color)

def update_position():
    global joystick
    mult = speed/framerate
    x_value = joystick.get_axis(0)
    y_value = 0 - joystick.get_axis(1)

    lights.current_target['x'] += x_value * mult
    lights.current_target['y'] += y_value * mult

def start_lights_thread():
    asyncio.run(lights.main())

def select_joystick():
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    joysticknames = [x.get_name() for x in joysticks]

    selected = questionary.select(
    "Select joystick",
    choices=joysticknames).ask()

    i = joysticknames.index(selected)

    return joysticks[i]

lights_thread = threading.Thread(target=start_lights_thread, daemon=True)
lights_thread.start()

joystick = select_joystick()

while running:
    update()
    update_position()
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lights.paused = not lights.paused
        if event.type == pygame.JOYBUTTONDOWN:
            lights.paused = not lights.paused
    clock.tick(framerate)