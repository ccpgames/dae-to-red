
class Axes(object):
    """
    The Collada format always uses a right-handed coordinate system.
    Format is RIGHT, FORWARD, UP.
    """
    Z_UP = ["X", "Y", "Z"]
    Y_UP = ["Z", "X", "Y"]

def get_axis_object_from_name(key):
    if key == "Z_UP":
        return Axes.Z_UP
    elif key == "Y_UP":
        return Axes.Y_UP
    else:
        raise ValueError("Unexpected axis name \"%s\"" % key)


class AxisConverter(object):
    def __init__(self, source_axis, target_axis):
        self.source_axis = source_axis
        self.target_axis = target_axis
        self.conversion_map = []
        for s in source_axis:
            for i, t in enumerate(target_axis):
                if s == t:
                    self.conversion_map.append(i)
        self.pitch_key = 'rotation' + chr(ord('X') + self.conversion_map[0])
        self.yaw_key =   'rotation' + chr(ord('X') + self.conversion_map[1])
        self.roll_key =  'rotation' + chr(ord('X') + self.conversion_map[2])

    def update_rotation_keys(self, keys):
        self.pitch_key = keys[0] or self.pitch_key
        self.yaw_key =   keys[1] or self.yaw_key
        self.roll_key =  keys[2] or self.roll_key


    def convert(self, coords):
        return [
            coords[self.conversion_map[0]],
            coords[self.conversion_map[1]],
            coords[self.conversion_map[2]],
        ]