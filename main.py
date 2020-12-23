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

# stage size
stage_min_x = config['display'].getfloat('stage_min_x')
stage_max_x = config['display'].getfloat('stage_max_x')
stage_min_y = config['display'].getfloat('stage_min_y')
stage_max_y = config['display'].getfloat('stage_max_y')

stage_width = stage_max_x - stage_min_x
stage_height = stage_max_y - stage_min_y

# Display framerate
framerate = config['display'].getint('framerate')

# Joystick sensitivity
speed = config['control'].getfloat('speed')

# Display scale & size
scale = config['display'].getint('scale')
size = width, height = int(stage_width*scale), int(stage_height*scale)

# show pan/tilt values on screen
show_pan_tilt = config['display'].getboolean('show_pan_tilt') 

# Init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# Init texts
font = pygame.font.SysFont('Calibri', 20)
pause_text = font.render('Output paused', False, (200, 200, 200))

running = True

# Translate "world" coordinates to pygame
def coordinate_translate(x: float, y: float) -> (int, int):
    x = x/stage_width
    y = y/stage_height

    y = 1 - y

    x = int(x*size[0] + size[0]/2)
    y = int(y*size[1] - size[1]/2)

    return (x, y)

# Renders text to surface
def render_text(text: str) -> pygame.Surface:
    global font
    return font.render(text, False, (200, 200, 200))


def update():
    screen.fill((10,10,10)) # Background
    tx, ty = coordinate_translate(lights.current_target['x'], lights.current_target['y']) # Target coords
    aa_circle(screen, tx, ty, 2*scale, (255,150,150)) # Target circle
    for f in lights.fixtures:
        x, y = coordinate_translate(f.x, f.y) # Fixture coords
        pygame.draw.aaline(screen, (50,100,50), (x, y), (tx, ty)) # Line from fixture to target 
        aa_circle(screen, x, y, scale, (150,255,150)) # Fixture circle

    # Pause text
    if lights.paused:
        screen.blit(pause_text,(20,20))

    # Pan tilt text
    if show_pan_tilt:
        t_pan = render_text(str(lights.fixtures[0].current_pan))
        t_tilt = render_text(str(lights.fixtures[0].current_tilt))
        screen.blit(t_pan,(20,50))
        screen.blit(t_tilt,(20,80))

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