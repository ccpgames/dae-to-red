import unittest
import axis

class TestAxis(unittest.TestCase):

    def test_y_up_to_z_up(self):
        converter = axis.AxisConverter(axis.Axes.Y_UP, axis.Axes.Z_UP)
        expected = [3,1,2]
        actual = converter.convert([1,2,3])
        self.assertEqual(expected, actual)

    def test_z_up_to_y_up(self):
        converter = axis.AxisConverter(axis.Axes.Z_UP, axis.Axes.Y_UP)
        expected = [2,3,1]
        actual = converter.convert([1,2,3])
        self.assertEqual(expected, actual)

    def test_z_up_to_z_up(self):
        converter = axis.AxisConverter(axis.Axes.Z_UP, axis.Axes.Z_UP)
        expected = [1,2,3]
        actual = converter.convert([1,2,3])
        self.assertEqual(expected, actual)

    def test_y_up_to_y_up(self):
        converter = axis.AxisConverter(axis.Axes.Y_UP, axis.Axes.Y_UP)
        expected = [1,2,3]
        actual = converter.convert([1,2,3])
        self.assertEqual(expected, actual)
