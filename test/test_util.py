import unittest
import util

class TestQuadraticBezierCurve(unittest.TestCase):
    def __init__(self, *args):
        super(TestQuadraticBezierCurve, self).__init__(*args)
        self.start_point = (0,0)
        self.end_point = (1,0)
        self.control_1 = (0,1)
        self.control_2 = (1,1)
        self.start_time = 1.0
        self.end_time = 2.0
        self.curve = util.QuadraticBezierCurve(
            self.start_point,
            self.end_point,
            self.control_1,
            self.end_point,
            self.start_time,
            self.end_time
        )

    def testTimeValueBeforeStartTimeEvaluatesToNone(self):
        self.assertEqual(self.curve.evaluate(0.9), None)

    def testTimeValueAfterEndTimeEvaluatesToNone(self):
        self.assertEqual(self.curve.evaluate(2.1), None)

    def testTimeValueAtStartTimeEvaluatesToStartPoint(self):
        expected = self.start_point
        actual = self.curve.evaluate(self.start_time)
        self.assertEqual(expected, actual)

    def testTimeValueAtEndTimeEvaluatesToEndPoint(self):
        expected = self.end_point
        actual = self.curve.evaluate(self.end_time)
        self.assertEqual(expected, actual)

    def testTimeValueInMiddleOfCurveEvaluatesCorrectly(self):
        expected = (0.5, 0.375)
        middle_of_curve = self.start_time + ((self.end_time - self.start_time) / 2.0)
        actual = self.curve.evaluate(middle_of_curve)
        self.assertEqual(expected, actual)

    def testToHermite(self):
        hermite = self.curve.to_hermite()
        for i in xrange(11):
            self.assertEqual(self.curve.evaluate(i), hermite.evaluate(i))