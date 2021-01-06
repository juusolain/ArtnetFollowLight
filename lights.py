import fixtureloader
import asyncio

fixtures = []

paused = False

current_target = {
    'x': -4,
    'y': 5,
    'z': 0
}

# Load fixtures
async def load():
    global fixtures
    fixtures, nodes = await fixtureloader.load() # Call fixtureloader to load

def set_positions():
    global current_target
    # set target for each of the fixtures
    for f in fixtures:
        f.set_target(current_target)

async def main():
    await load() # Load fixtures
    while True:
        if not paused:
            set_positions()
        await asyncio.sleep(1/30) # update position 30 times in a second

# Set target
async def set_target(new_target):
    global current_target
    current_target = new_target