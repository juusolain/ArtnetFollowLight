import math
from typing import List

class Coordinates:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

# Get pan from distances
def get_pan(delta_x: float, delta_y: float) -> float:
    return math.degrees(math.atan2(delta_x, delta_y))

# Get tilt from distances
def get_tilt(delta_x: float, delta_y: float, delta_z: float) -> float:
    dist = math.hypot(delta_x, delta_y)
    return math.degrees(math.atan2(dist, delta_z))

# Get distances between two points
def get_deltas(origin: Coordinates, dest: Coordinates) -> Coordinates:
    x = dest.x - origin.x
    y = dest.y - origin.y
    z = origin.z - dest.z
    return Coordinates(x, y, z)

# Convert to uint from 0 to 256^width
def convert_to_uint(value_deg: int, min_deg=-180, max_deg=180, width=1) -> int: 
    dist_from_min = value_deg - min_deg
    dist_max = max_deg - min_deg
    normalized_dist = dist_from_min/dist_max
    max_int = 256**width
    return round(normalized_dist*max_int)

# Convert uint to uint8array for DMX
def uint_to_array(value: int, width=1,) -> List[int]:
    # Init array
    arr = []
    
    # Value checks
    if value > 256 ** width or value < 0:
        raise ValueError("Cannot convert to uint8array, value is too small or too large")

    # Divide by 256 to get individual array values
    for i in range(width):
        modval = value % 256
        arr.append(modval)
        value -= modval
        value = int(value / 256)

    # Reverse to make it little-endian
    arr.reverse()
    return arr