def float_equal(f1, f2):
    return abs(f1 - f2) <= 0.0000000001

def point2d_equal(p0, p1):
    return float_equal(p0[0], p1[0]) and float_equal(p0[1], p1[1])

class QuadraticHermiteCurve(object):
    def __init__(self, p0, p1, c0, c1, start_time, end_time):
        self.start_value = p0
        self.end_value = p1
        self.control_1 = c0
        self.control_2 = c1
        self.start_time = start_time
        self.end_time = end_time

    def evaluate(self, t):
        if t < self.start_time:
            return None
        elif t > self.end_time:
            return None

        normalized_time = (t - self.start_time) / (self.end_time - self.start_time)

        x1 = self.start_value[0] * (2 * normalized_time ** 3 - 3 * normalized_time ** 2 + 1)
        x2 = self.control_1[0]  * (normalized_time ** 3 - 2 * normalized_time ** 2 + normalized_time)
        x3 = self.end_value[0] * (-2 * normalized_time ** 3 + 3 * normalized_time ** 2)
        x4 = self.control_2[0] * (normalized_time ** 3 - normalized_time ** 2)

        y1 = self.start_value[1] * (2 * normalized_time ** 3 - 3 * normalized_time ** 2 + 1)
        y2 = self.control_1[1]  * (normalized_time ** 3 - 2 * normalized_time ** 2 + normalized_time)
        y3 = self.end_value[1] * (-2 * normalized_time ** 3 + 3 * normalized_time ** 2)
        y4 = self.control_2[1] * (normalized_time ** 3 - normalized_time ** 2)

        return (x1+x2+x3+x4, y1+y2+y3+y4)

    def __eq__(self, other):
        return (
            self.start_value == other.start_value and
            self.end_value == other.end_value and
            point2d_equal(self.control_1, other.control_1) and
            point2d_equal(self.control_2, other.control_2) and
            self.start_time == other.start_time and
            self.end_time == other.end_time
        )

class QuadraticBezierCurve(object):
    def __init__(self, p0, p1, c0, c1, start_time, end_time):
        self.start_value = p0
        self.end_value = p1
        self.control_1 = c0
        self.control_2 = c1
        self.start_time = start_time
        self.end_time = end_time

    def to_hermite(self):
        return QuadraticHermiteCurve(
            self.start_value,
            self.end_value,
            (3.0 * (self.control_1[0] - self.start_value[0]), 3.0 * (self.control_1[1] - self.start_value[1])),
            (3.0 * (self.end_value[0] - self.control_2[0]), 3.0 * (self.end_value[1] - self.control_2[1])),
            self.start_time,
            self.end_time
        )

    def evaluate(self, t):
        if t < self.start_time:
            return None
        elif t > self.end_time:
            return None

        normalized_time = (t - self.start_time) / (self.end_time - self.start_time)

        x1 = self.start_value[0] * (1 - normalized_time)**3
        x2 = 3 * self.control_1[0] * normalized_time * (1 - normalized_time)**2
        x3 = 3 * self.control_2[0] * normalized_time ** 2 * (1 - normalized_time)
        x4 = self.end_value[0] * normalized_time ** 3

        y1 = self.start_value[1] * (1 - normalized_time)**3
        y2 = 3 * self.control_1[1] * normalized_time * (1 - normalized_time)**2
        y3 = 3 * self.control_2[1] * normalized_time ** 2 * (1 - normalized_time)
        y4 = self.end_value[1] * normalized_time ** 3
        return (x1+x2+x3+x4, y1+y2+y3+y4)

    def __eq__(self, other):
        return (
            self.start_value == other.start_value and
            self.end_value == other.end_value and
            self.control_1 == other.control_1 and
            self.control_2 == other.control_2 and
            self.start_time == other.start_time and
            self.end_time == other.end_time
        )

    def __repr__(self):
        return """QuadraticBezierCurve:
        {
            start_value: {start_value}
            end_value: {end_value}
            control_1: {self.control_1}
            control_2: {self.control_2}
            start_time: {start_time}
            end_time: {end_time}
        }
        """.format(
                   start_value = self.start_value,
                   end_value = self.end_value,
                   control_1 = self.control_1,
                   control_2 = self.control_2,
                   start_time = self.start_time,
                   end_time = self.end_time
        )

def get_all(key, *args):
    return [i[key] for i in args]