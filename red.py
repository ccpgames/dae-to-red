import templates
import util


class EveSpaceScene():
    def __init__(self):
        self.curve_sets = []
    def __str__(self):
        s = templates.eve_space_scene
        if self.curve_sets:
            s += "\ncurveSets:"
        for i in self.curve_sets:
            s += str(i)
        return s


class Tr2ScalarKey(object):
    def __init__(self, time, value, left_tangent, right_tangent):
        self.time = time
        self.value = value
        self.left_tangent = left_tangent
        self.right_tangent = right_tangent

    def __str__(self):
        return templates.scalar_key.format(
            time=self.time,
            value=self.value,
            left_tangent=self.left_tangent,
            right_tangent=self.right_tangent,
            )

    def __eq__(self, other):
        return (
            util.float_equal(self.time, other.time) and
            util.float_equal(self.value, other.value)
        )


class Tr2ScalarCurve(object):
    def __init__(self, curve_type, time_offset, length, start_value, end_value, start_tangent, end_tangent):
        self.curve_type = curve_type
        self.time_offset = time_offset
        self.length = length
        self.start_value = start_value
        self.end_value = end_value
        self.start_tangent = start_tangent
        self.end_tangent = end_tangent
        self.scalar_keys = []

    def __str__(self):
        s = templates.rotation_curve_header.format(
            curve_type=self.curve_type,
            length=self.length,
            start_value=self.start_value,
            end_value=self.end_value,
            start_tangent=self.start_tangent,
            end_tangent=self.end_tangent,
            time_offset=self.time_offset,
            )
        if self.scalar_keys:
            s += "\n        keys:"
        for i in self.scalar_keys:
            s += str(i)

        return s

    def __eq__(self, other):
        return (
            self.curve_type == other.curve_type and
            util.float_equal(self.length, other.length) and
            util.float_equal(self.start_value, other.start_value) and
            util.float_equal(self.end_value, other.end_value) and
            util.float_equal(self.start_tangent, other.start_tangent) and
            util.float_equal(self.end_tangent, other.end_tangent) and
            util.float_equal(self.time_offset, other.time_offset)
        )

class Tr2EulerRotation(object):
    def __init__(self, object_name, yaw, pitch, roll):
        self.object_name = object_name
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self):
        s = templates.euler_rotation_header.format(
            object_name=self.object_name
        )
        if self.yaw is not None:
            s += self.yaw.__str__()
        if self.pitch is not None:
            s += self.pitch.__str__()
        if self.roll is not None:
            s += self.roll.__str__()
        return s

    def __eq__(self, other):
        return (
            self.object_name == other.object_name and
            self.yaw == other.yaw and
            self.pitch == other.pitch and
            self.roll == other.roll
        )

class Tr2VectorKey(object):
    def __init__(self, object_name, value, right_tangent, left_tangent, time):
        self.object_name = object_name
        self.value = value
        self.right_tangent = right_tangent
        self.left_tangent = left_tangent
        self.time = time


    def __str__(self):
        return templates.vector_key.format(
            object_name=self.object_name,
            value=self.value,
            right_tangent=self.right_tangent,
            left_tangent=self.left_tangent,
            time=self.time
            )

    def __eq__(self, other):
        return (
            self.object_name == other.object_name and
            self.length == other.length and
            self.value == other.value and
            self.end_value == other.end_value and
            self.left_tangent == other.left_tangent and
            self.right_tangent == other.right_tangent and
            self.time == other.time
        )

class Tr2VectorCurve(object):
    def __init__(self, object_name, time_offset, length, start_value, end_value, start_tangent, end_tangent):
        self.object_name = object_name
        self.time_offset = time_offset
        self.length = length
        self.start_value = start_value
        self.end_value = end_value
        self.start_tangent = start_tangent
        self.end_tangent = end_tangent
        self.keys = []

    def __str__(self):
        s = templates.location_curve_header.format(
            object_name=self.object_name,
            time_offset=self.time_offset,
            length=self.length,
            start_value=self.start_value,
            end_value=self.end_value,
            start_tangent=self.start_tangent,
            end_tangent=self.end_tangent,
        )
        if self.keys:
            s += "\n    keys:"
            for i in self.keys:
                s += str(i)
        return s

    def __eq__(self, other):
        return (
            self.object_name == other.object_name and
            self.length == other.length and
            self.time_offset == other.time_offset and
            self.start_value == other.start_value and
            self.end_value == other.end_value and
            self.start_tangent == other.start_tangent and
            self.end_tangent == other.end_tangent
        )


class TriCurveSet(object):
    def __init__(self, object_name):
        self.object_name = object_name
        self.curves = []

    def __str__(self):
        s = templates.curve_set_header.format(object_name=self.object_name)
        for c in self.curves:
            s += c.__str__()
        return s

    def __eq__(self, other):
        return (
            self.object_name == other.object_name and
            self.curves == other.curves
        )
    def __repr__(self):
        return """TriCurveSet
        {
            {object_name}
            {curves}
        }
        """.format(
            object_name = self.object_name,
            curves = self.curves
        )