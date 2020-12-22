import configparser
import os
from pyartnet import ArtNetNode
from fixture import Fixture

async def load():
    fixtures = []
    nodes = {}
    for dirpath, dirs, files in os.walk("./active/"):
        for filename in files:
            fname = os.path.join(dirpath,filename)
            config = configparser.ConfigParser()
            config.read(fname)
            fixtureconfig = {}
            for key in config['position']:
                fixtureconfig[key] = float(config['position'][key])
            for key in config['channels']:
                fixtureconfig[key] = int(config['channels'][key])
            for key in config['location']:
                fixtureconfig[key] = float(config['location'][key])
            
            fixtureconfig['start_channel'] = int(config['DMX']['start_channel'])
            fixtureconfig['universe'] = int(config['DMX']['universe'])
            fixtureconfig['node_ip'] = config['DMX']['node_ip']

            fixtureconfig['prefer_pan'] = config['misc'].getboolean('prefer_pan')
            fixtureconfig['default_fade_time'] = int(config['misc']['default_fade_time'])
            fixtureconfig['invert_tilt'] = config['misc'].getboolean('invert_tilt')
            fixtureconfig['invert_pan'] = config['misc'].getboolean('invert_pan')
                

            node_ip = fixtureconfig['node_ip']
            universe = fixtureconfig['universe']
            if not node_ip in nodes:
                nodeobj = ArtNetNode(node_ip)
                await nodeobj.start()
                nodes[node_ip] = {
                    'node': nodeobj,
                    'universes': {}
                }
            if not universe in nodes[node_ip]['universes']:
                nodeobj = nodes[node_ip]['node']
                universeobj = nodeobj.add_universe(universe)
                nodes[node_ip]['universes'][universe] = universeobj

            fixture = Fixture(fixtureconfig)
            fixture.start(nodes[node_ip]['universes'][universe])

            fixtures.append(fixture)
    return (fixtures, nodes)
