import configparser
from fixture import Fixture
from typing import List
import lights
import asyncio
import threading
import pygame
from pygame import gfxdraw
import questionary
import listener
import random
import listener


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
joystick_speed = config['control'].getfloat('speed')
joystick_deadzone = config['control'].getfloat('deadzone')
random_debug_input = config['control'].getboolean('random_debug_input')

# Joystick buttons
joystick_button_next = config['control'].getint('button_next')
joystick_button_prev = config['control'].getint('button_prev')
joystick_button_reset = config['control'].getint('button_reset')

# Display scale & size
scale = config['display'].getint('scale')
size = width, height = int(stage_width*scale), int(stage_height*scale)

# show pan/tilt values on screen
show_pan_tilt = config['display'].getboolean('show_pan_tilt') 
selected_fixture_index = 0

# Init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# Init texts
font = pygame.font.SysFont('Calibri', 20)
pause_text = font.render('Output paused', True, (200, 200, 200))

# Main running bool
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
    return font.render(text, True, (200, 200, 200))


def update() -> None:
    screen.fill((10,10,10)) # Background
    tx, ty = coordinate_translate(lights.current_target['x'], lights.current_target['y']) # Target coords
    aa_circle(screen, tx, ty, 2*scale, (255,150,150)) # Target circle
    for f in lights.fixtures:
        x, y = coordinate_translate(f.x, f.y) # Fixture coords
        pygame.draw.aaline(screen, (50,100,50), (x, y), (tx, ty)) # Line from fixture to target 
        aa_circle(screen, x, y, scale, (150,255,150)) # Fixture circle

    # Pause text
    if listener.paused:
        screen.blit(pause_text, (20, size[1]-40))

    # Pan tilt text
    if show_pan_tilt and len(lights.fixtures) > 0:
        t_debug_title = render_text(f'F[{selected_fixture_index}]: Pan & tilt:')
        t_pan = render_text(str(round(lights.fixtures[selected_fixture_index].current_pan, 2)))
        t_tilt = render_text(str(round(lights.fixtures[selected_fixture_index].current_tilt, 2)))
        screen.blit(t_debug_title,(20,20))
        screen.blit(t_pan,(20,40))
        screen.blit(t_tilt,(20,60))

    pygame.display.flip()

# Antialiased circle
def aa_circle(surf: pygame.surface, x: int, y: int, radius: int, color: (int, int, int)) -> None:
    gfxdraw.filled_circle(surf, x, y, radius, color)
    gfxdraw.aacircle(surf, x, y, radius, color)

# Update target from joystick
def update_position() -> None:
    global joystick
    if joystick is None: # If no joystick, random inputs for debugs
        if random_debug_input:
            x_value = random.uniform(-0.5, 0.5)
            y_value = random.uniform(-0.5, 0.5)
        else:
            return
    else:
        x_value = joystick.get_axis(0)
        y_value = 0 - joystick.get_axis(1)
    mult = joystick_speed / framerate
    

    if abs(x_value) < joystick_deadzone or abs(y_value) < joystick_deadzone:
        return
        

    lights.current_target['x'] += x_value * mult
    lights.current_target['y'] += y_value * mult

# Start light thread
def start_lights_thread() -> None:
    asyncio.run(lights.main())

def start_listener_thread() -> None:
    listener.main()

# Select joystick if multiple
def select_joystick() -> pygame.joystick.Joystick:
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    # If only one connected, select it
    if len(joysticks) == 1:
        return joysticks[0]
    
    # If no joysticks...
    if len(joysticks) == 0:
        print('No joysticks connected...')
        return None

    joysticknames = [x.get_name() for x in joysticks]

    selected = questionary.select(
    "Select joystick",
    choices=joysticknames).ask()

    i = joysticknames.index(selected)

    return joysticks[i]

# Start light thread
lights_thread = threading.Thread(target=start_lights_thread, daemon=True)
lights_thread.start()

# Start listener thread
listener_thread = threading.Thread(target=start_listener_thread, daemon=True)
listener_thread.start()

# Select joystick
joystick = select_joystick()

# Main loop
while running:
    # Update screen & target
    update()
    update_position()

    # Events
    ev = pygame.event.get()
    for event in ev:
        # Quit from pygame
        if event.type == pygame.QUIT:
            running = False
        # Keyboard
        if event.type == pygame.KEYDOWN:
            # Pause
            if event.key == pygame.K_SPACE:
                lights.paused = not lights.paused
        # Joystick buttons
        if event.type == pygame.JOYBUTTONDOWN:
            # Pause
            if event.button == joystick_button_next:
                selected_fixture_index += 1
                if selected_fixture_index > len(lights.fixtures) - 1:
                    selected_fixture_index = 0
            if event.button == joystick_button_prev:
                selected_fixture_index -= 1
                if selected_fixture_index < 0:
                    selected_fixture_index = len(lights.fixtures) - 1
            if event.button == joystick_button_reset:
                lights.reset_target()

    # Clock tick
    clock.tick(framerate)