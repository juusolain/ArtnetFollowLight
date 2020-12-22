import fixtureloader
import asyncio

fixtures = []

paused = False

current_target = {
    'x': -4,
    'y': 5,
    'z': 0
}

async def load():
    global fixtures
    fixtures, nodes = await fixtureloader.load()

def set_positions():
    global current_target
    for f in fixtures:
        f.set_target(current_target['x'], current_target['y'], current_target['z'])

async def main():
    global fixtures
    await load()
    while True:
        if not paused:
            set_positions()
        await asyncio.sleep(0.05) # update position 20 times in a second

async def set_target(new_target):
    global current_target
    current_target = new_target