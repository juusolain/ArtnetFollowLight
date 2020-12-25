# Artnet follow light
## End goal:
* Fully automatic follow spot using existing or cheap equipment

## Current TODO:
- [x] Fixture class basic implementation
- [x] Fixture config loading from files
- [x] Universe and node setup
- [x] Control with joystick

# Node setup:
If you are using another console to output other values, you should change the merge mode on the console to LTP. Otherwise the outputted pan & tilt values could be overridden by the other console.

# Config

## User settings
See config.ini.template

Config should be placed in the config.ini file.

    [display]
    stage_min_x = -20
    stage_max_x = 20
    stage_min_y = -10
    stage_max_y = 20

    framerate = 60
    scale = 20

    [control]
    speed = 10

## Fixture config
Copy a template ini from templates/ or create your own ini in active. The following values should always be configured individually for each fixture:

    start_channel
    x
    y
    z
    universe
    node_ip
    
### DMX address, universe and node
Set the starting address of the fixture, the universe in which the fixture and the IP address of the node

    start_channel=1
    universe=1
    node_ip=10.0.0.1

### Misc
Set default fade time for this fixture and whether to prefer tilt or pan.
Prefer pan is used to set, whether the pan or tilt range should be preferred when rotating. When yes, the tilt range starts from zero, and when no, the pan range is limited to -90 degrees ->90 degrees

    default_fade_time = 50
    prefer_pan = yes

### Location
The x, y and z coordinates of the fixture need to be configured.
Use the variables x, y and z

    x=10
    y=0
    z=5

### Position offsets
You should choose an origin point and the orientation of the coordinates. It is recommended that you point the X-axis along the stage and the Z-axis up.

In the default position, the position model's forward vector is (0,0,-1) and the up vector is (0,1,0). More simply, the model points down (Z-), and the top of the fixture points forward (Y+). The fixture needs to be offsetted to this position if it doesn't do it by default.

    tilt_offset=0
    pan_offset=0

### DMX channel configuration
You can look up these in the manual of your fixture.

Example (GLP S350 in 35 DMX mode):

    pan_start = 1
    pan_width = 2
    pan_min_degrees = -282.5
    pan_max_degrees = 282.5
    tilt_start = 3
    tilt_width = 2
    pan_min_degrees = -180
    pan_max_degrees = 180

