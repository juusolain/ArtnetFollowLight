import calc
import collections

class Fixture:
    # Config default values
    pan_offset = 0
    tilt_offset = 0
    pan_start = 1
    tilt_start = 3
    pan_width = 2
    tilt_width = 2
    pan_min_degrees = -180
    pan_max_degrees = 180
    tilt_min_degrees = -180
    tilt_max_degrees = 180
    x = 0
    y = 0
    z = 0
    start_channel = 1
    default_fade_time = 50 
    prefer_tilt = False
    invert_pan = False
    invert_tilt = True

    # Props
    current_pan = 0
    current_tilt = 0

    # Set fixture config values
    def __init__(self, config) -> None:
        # Set attributes from config
        for key, value in config.items():
            setattr(self, key, value)

    # Stat
    def start(self, universe) -> None:
        # Init channels
        self.pan_channel = universe.add_channel(start=self.pan_start + self.start_channel, width=self.pan_width)
        self.tilt_channel = universe.add_channel(start=self.tilt_start + self.start_channel, width=self.tilt_width)

    # Calculate pan & tilt from target coords and send to fixture
    def set_target(self, new_target: dict, fade_time=default_fade_time):
        # Get XYZ from target
        x = new_target['x']
        y = new_target['y']
        z = new_target['z']
        
        # Calculate differences between fixture and target coordinates
        deltas = calc.get_deltas(calc.Coordinates(self.x, self.y, self.z), calc.Coordinates(x, y, z))

        # Calculate raw pan & tilt from deltas
        pan = calc.get_pan(deltas.x, deltas.y)
        tilt = calc.get_tilt(deltas.x, deltas.y, deltas.z)

        # Use full tilt range if enabled
        if self.prefer_tilt:
            if pan > 90:
                pan -= 180
                tilt = - tilt
            if pan < -90:
                pan += 180
                tilt = - tilt

        # Pan & tilt inverts
        if self.invert_tilt:
            tilt = - tilt

        if self.invert_pan:
            pan = - pan

        # Pan & tilts offsets
        pan += self.pan_offset
        tilt += self.tilt_offset
        
        # Send pan & tilt to fixture
        self.set_position_raw(pan, tilt, fade_time)

    # Send pan & tilt to fixture on DMX
    def set_position_raw(self, pan: float, tilt: float, fade_time: int) -> None:
        # Set cached pan & tilt
        self.current_pan = pan
        self.current_tilt = tilt

        # Convert to DMX uint
        pan_uint = calc.convert_to_uint(pan, min_deg=self.pan_min_degrees, max_deg=self.pan_max_degrees, width=self.pan_width)
        tilt_uint = calc.convert_to_uint(tilt, min_deg=self.tilt_min_degrees, max_deg=self.tilt_max_degrees, width=self.tilt_width)

        # Convert to uint8 array for multiple DMX channels
        pan_arr = calc.uint_to_array(pan_uint, self.pan_width)
        tilt_arr = calc.uint_to_array(tilt_uint, self.tilt_width)

        # Send pan & tilt to channels
        self.pan_channel.add_fade(pan_arr, fade_time)
        self.tilt_channel.add_fade(tilt_arr, fade_time)







