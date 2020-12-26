# Artnet follow light
## End goal:
* Fully automatic follow spot using existing or cheap equipment

## Current TODO:
- [ ] Make fixture loading better
- [ ] Configuration UI

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

    show_pan_tilt = yes

    [control]
    speed = 10
    deadzone = 0.01
    button_pause = 1

## Fixture config
Copy a template ini from templates/ or create your own ini in active. The following values should always be configured individually for each fixture:

    start_channel
    x
    y
    z
    universe
    node_ip
    
The values in the examples below are for the GLP impression S350.

### DMX address, universe and node
Set the starting address of the fixture, the universe in which the fixture and the IP address of the node

    [DMX]
    start_channel = 1
    universe = 1
    node_ip = 10.0.0.1

### Misc
Set default fade time for this fixture and whether to prefer tilt or pan.
Prefer tilt is used to set whether the pan or tilt range should be preferred when rotating. Depending on the fixture location pan or tilt should be chosen to be preferred.

    [misc]
    default_fade_time = 50
    prefer_tilt = no

### Location
The x, y and z coordinates of the fixture need to be configured.
Use the variables x, y and z

    [location]
    x = 10
    y = 0
    z = 5

### Pan and tilt offsets
You might need to modify these depending on how the fixture is orientated.

    [position]
    tilt_offset = 0
    pan_offset = 0

### Pan and tilt inverts
These might also be need to be modified based on the orientation of the fixture.

    [misc]
    tilt_invert = yes
    pan_invert = no

### Pan and tilt limits:

    [position]
    pan_min_degrees = -282.5
    pan_max_degrees = 282.5
    tilt_min_degrees = -180
    tilt_max_degrees = 180

### DMX channel configuration
You can look up these in the manual of your fixture.
    
    [channels]
    pan_start = 0
    pan_width = 2
    tilt_start = 2
    tilt_width = 2

