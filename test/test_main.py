

import unittest

from dae_to_red import axis
from dae_to_red import colladamunge
from dae_to_red import main
from dae_to_red import red
from dae_to_red import util

import example_data


class TestReadCurveDataFromAnimation(unittest.TestCase):
    def test_animation_with_no_samplers_has_no_effect(self):
        animation = colladamunge.Animation({}, {}, [], [])
        curves = []
        main.read_curve_data_from_animation(animation, curves)
        expected = []
        self.assertEqual(expected, curves)

    def test_animation_with_unsupported_curve_type_raises(self):
        sources = example_data.get_sources()
        sources["Cube_location_X-interpolation"].values[0] = "AN_UNSUPPORTED_TYPE_FOR_SURE"
        channels = example_data.get_channels()
        samplers = example_data.get_samplers()
        animations = example_data.get_animations()
        animation = colladamunge.Animation(sources, channels, samplers, animations)
        self.assertRaises(RuntimeError, main.read_curve_data_from_animation, animation, {})

    def test_animation(self):
        self.maxDiff = None
        sources = example_data.get_sources()
        channels = example_data.get_channels()
        samplers = example_data.get_samplers()
        animations = example_data.get_animations()
        animation = colladamunge.Animation(sources, channels, samplers, animations)
        curves = {}
        main.read_curve_data_from_animation(animation, curves)
        expected = {
            'Cube': {
                'location': {
                    'X': [
                        util.QuadraticHermiteCurve(
                            (0.04166662, 0.03813225),
                            (0.8333333, 0.03813225),
                            (0.92722734, 0.0),
                            (0.92722710, 0.0),
                            0.04166662,
                            0.8333333),
                        util.QuadraticHermiteCurve(
                            (0.8333333, 0.03813225),
                            (5.458333, 0.03813225),
                            (-1.4477727, 0.0),
                            (14.8022261, 0.0),
                            0.8333333,
                            5.458333),
                        util.QuadraticHermiteCurve(
                            (5.458333, 0.03813225),
                            (9.875, 0.03813225),
                            (-15.3227718, 0.0),
                            (28.052227199999997, 0.0),
                            5.458333,
                            9.875),
                        ]
                }
            }
        }
        for i, v in enumerate(expected['Cube']['location']['X']):
            print expected['Cube']['location']['X'][i]
            print "#########"
            print curves['Cube']['location']['X'][i]
        self.assertEqual(expected, curves)

class TestEvaluateCurveValues(unittest.TestCase):
    def testEmptyCurveListResultsInEmptyDict(self):
        expected = {}
        actual = main.evaluate_curve_values([])
        self.assertDictEqual(expected, actual)

    def testEvaluateSingleCurve(self):
        expected = {
            'Cube': {
                'location': {
                    'X': {
                        0:
                            {
                                'control_1': (0, 1),
                                'control_2': (1, 1),
                                'end_time': 2.0,
                                'end_value': 0,
                                'start_time': 1.0,
                                'start_value': 0
                            }
                    }
                }
            }
        }
        curve = util.QuadraticHermiteCurve(
            (0,0),(1,0),
            (0,1),(1,1),
            1.0,
            2.0)
        actual = main.evaluate_curve_values({'Cube': {'location': {'X': [curve]}}})
        self.assertDictEqual(expected, actual)


class TestObjectConverter(unittest.TestCase):
    def setUp(self):
        self.axis_converter = axis.AxisConverter(axis.Axes.Z_UP, axis.Axes.Y_UP)

    def testConvertTranslation(self):
        data = {
            'location': {
                'X': {0: {"start_time": 0.0, "start_value": 0.0, "end_time": 2.0, "end_value": 2.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}},
                'Y': {0: {"start_time": 0.0, "start_value": 3.0, "end_time": 2.0, "end_value": 5.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}},
                'Z': {0: {"start_time": 0.0, "start_value": 6.0, "end_time": 2.0, "end_value": 8.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}},
                }
        }
        node = colladamunge.Node()
        node.axis_translations = [('location', [0,0,0]),('location', [0,0,0]),('location', [0,0,0])]
        converter = main.ObjectConverter(node, data, "MyObject", self.axis_converter)

        expected_start_tangent = [2.6666666666666665, 2.6666666666666665, 2.6666666666666665]
        expected_end_tangent = [0.0, 0.0, 0.0]
        expected_vector_curve = red.Tr2VectorCurve("MyObject", 0.0, 2.0, 0.0, 2.0, expected_start_tangent, expected_end_tangent)
        expected_vector_curve.start_value = [3.0, 6.0, 0.0]
        expected_vector_curve.end_value = [5.0, 8.0, 2.0]

        expected = red.TriCurveSet("MyObject")
        expected.curves = [expected_vector_curve]
        actual = converter.convert_object()

        self.assertEqual(expected, actual)

    def testConvertRotation(self):
        data = {
            'rotationX': {'ANGLE': {0: {"start_time": 0.0, "start_value": 1.0, "end_time": 2.0, "end_value": 3.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}}},
            'rotationY': {'ANGLE': {0: {"start_time": 0.0, "start_value": 4.0, "end_time": 2.0, "end_value": 6.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}}},
            'rotationZ': {'ANGLE': {0: {"start_time": 0.0, "start_value": 7.0, "end_time": 2.0, "end_value": 9.0, "control_1": (3.0, 4.0), "control_2": (5.0, 6.0)}}},
        }
        node = colladamunge.Node()
        node.axis_rotations = [('rotationX', 0),('rotationY', 1),('rotationZ', 2)]
        converter = main.ObjectConverter(node, data, "MyObject", self.axis_converter)

        roll = red.Tr2ScalarCurve("rollCurve",   0.0, 2.0, 0.0174532925199, 0.0523598775598, 2.66666666667, 2.4)
        pitch = red.Tr2ScalarCurve("pitchCurve", 0.0, 2.0, 0.0698131700798, 0.10471975512,   2.66666666667, 2.4)
        yaw = red.Tr2ScalarCurve("yawCurve",     0.0, 2.0, 0.12217304764, 0.157079632679,  2.66666666667, 2.4)

        euler_rotation = red.Tr2EulerRotation("MyObject", yaw, pitch, roll)

        expected = red.TriCurveSet("MyObject")
        expected.curves = [euler_rotation]
        actual = converter.convert_object()
        self.assertEqual(expected, actual)


