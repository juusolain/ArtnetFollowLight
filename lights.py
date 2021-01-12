import fixtureloader
import asyncio
import listener
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

fixtures = []

default_target = {
    'x': config['target'].getfloat('x'),
    'y': config['target'].getfloat('y'),
    'z': config['target'].getfloat('z')
}

current_target = default_target.copy()
# Load fixtures
async def load():
    global fixtures
    fixtures, nodes = await fixtureloader.load() # Call fixtureloader to load

def set_positions():
    global current_target
    # set target for each of the fixtures
    for f in fixtures:
        f.set_target(current_target)

def reset_target():
    global current_target
    current_target = default_target.copy()

async def main():
    await load() # Load fixtures
    while True:
        if not listener.paused:
            set_positions()
        await asyncio.sleep(1/44) # update position 30 times in a second

# Set target
async def set_target(new_target):
    global current_target
    current_target = new_target