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

    # Props
    current_pan = 0
    current_tilt = 0

    # Set fixture config values
    def __init__(self, config) -> None:
        for key, value in config.items():
            setattr(self, key, value)

    # Stat
    def start(self, universe) -> None:
        self.pan_channel = universe.add_channel(start=self.pan_start + self.start_channel, width=self.pan_width)
        self.tilt_channel = universe.add_channel(start=self.tilt_start + self.start_channel, width=self.tilt_width)

    def set_target(self, x: float, y: float, z: float, fade_time=None):
        if fade_time is None:
            fade_time = self.default_fade_time
        deltas = calc.get_deltas(calc.Coordinates(self.x, self.y, self.z), calc.Coordinates(x, y, z))
        pan = calc.get_pan(deltas.x, deltas.y)
        tilt = calc.get_tilt(deltas.x, deltas.y, deltas.z)

        # Faster movement below lamp if not disabled
        if self.prefer_tilt:
            if pan > 90:
                pan -= 180
                tilt = - tilt
            if pan < -90:
                pan += 180
                tilt = - tilt

        if self.invert_tilt:
            tilt = - tilt

        if self.invert_pan:
            pan = - pan

        self.current_pan = pan
        self.current_tilt = tilt

        pan += self.pan_offset
        tilt += self.tilt_offset

        self.set_position_raw(pan, tilt, fade_time)

    def set_position_raw(self, pan: float, tilt: float, fade_time: int) -> None:
        tilt = - tilt
        pan_int = calc.convert_to_int(pan, min_deg=self.pan_min_degrees, max_deg=self.pan_max_degrees, width=self.pan_width)
        tilt_int = calc.convert_to_int(tilt, min_deg=self.tilt_min_degrees, max_deg=self.tilt_max_degrees, width=self.tilt_width)

        pan_arr = calc.int_to_array(pan_int, self.pan_width)
        tilt_arr = calc.int_to_array(tilt_int, self.tilt_width)

        self.pan_channel.add_fade(pan_arr, fade_time)
        self.tilt_channel.add_fade(tilt_arr, fade_time)







