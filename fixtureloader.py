import configparser
import os
from pyartnet import ArtNetNode
from fixture import Fixture

# Load all fixtures
async def load():
    # Init fixture array & node dict
    fixtures = []
    nodes = {}
    for dirpath, dirs, files in os.walk("./active/"):
        for filename in files:
            # Load config file
            fname = os.path.join(dirpath,filename)
            config = configparser.ConfigParser()
            config.read(fname)

            # Init fixtureconfig object
            fixtureconfig = {}

            # Load values from config to fixtureconfig
            # Needs to made prettier
            for key in config['position']:
                fixtureconfig[key] = float(config['position'][key])
            for key in config['channels']:
                fixtureconfig[key] = int(config['channels'][key])
            for key in config['location']:
                fixtureconfig[key] = float(config['location'][key])
            
            fixtureconfig['start_channel'] = int(config['DMX']['start_channel'])
            fixtureconfig['universe'] = int(config['DMX']['universe'])
            fixtureconfig['node_ip'] = config['DMX']['node_ip']

            fixtureconfig['prefer_tilt'] = config['misc'].getboolean('prefer_tilt')
            fixtureconfig['default_fade_time'] = int(config['misc']['default_fade_time'])
            fixtureconfig['invert_tilt'] = config['misc'].getboolean('invert_tilt')
            fixtureconfig['invert_pan'] = config['misc'].getboolean('invert_pan')
            
            node_ip = fixtureconfig['node_ip']
            universe = fixtureconfig['universe']

            # Create node, universe and fixture objects
            if not node_ip in nodes:
                # Create new node if it doesn't exist
                nodeobj = ArtNetNode(node_ip)
                await nodeobj.start()
                nodes[node_ip] = {
                    'node': nodeobj,
                    'universes': {}
                }
            if not universe in nodes[node_ip]['universes']:
                # Create new universe if it doesn't exist
                nodeobj = nodes[node_ip]['node']
                universeobj = nodeobj.add_universe(universe)
                nodes[node_ip]['universes'][universe] = universeobj
            
            # Create fixture and init
            fixture = Fixture(fixtureconfig)
            fixture.start(nodes[node_ip]['universes'][universe])

            fixtures.append(fixture)
    return (fixtures, nodes)
