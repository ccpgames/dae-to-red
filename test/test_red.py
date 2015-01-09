import unittest
import red

class TestTr2Tr2ScalarCurve(unittest.TestCase):
    def test_str(self):
        curve = red.Tr2ScalarCurve("yawCurve", 0.0, 2, 0, 1, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        expected = """
        yawCurve:
            type: Tr2ScalarCurve
            length: 2
            cycle: 0
            timeScale: 1.0
            startValue: 0
            endValue: 1
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0"""
        actual = curve.__str__()
        self.assertEqual(expected, actual)

class TestTr2EulerRotation(unittest.TestCase):
    def test_str_yaw_curve(self):
        yaw = red.Tr2ScalarCurve("yawCurve", 0.0, 2, 0, 1, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        rot = red.Tr2EulerRotation("MyRotation", yaw, None, None)
        expected = """
    - &euler_rotation_MyRotation
        type: Tr2EulerRotation
        yawCurve:
            type: Tr2ScalarCurve
            length: 2
            cycle: 0
            timeScale: 1.0
            startValue: 0
            endValue: 1
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0"""
        actual = rot.__str__()
        self.assertEqual(expected, actual)

    def test_str_pitch_curve(self):
        pitch = red.Tr2ScalarCurve("pitchCurve", 0.0, 2, 0, 1, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        rot = red.Tr2EulerRotation("MyRotation", None, pitch, None)
        expected = """
    - &euler_rotation_MyRotation
        type: Tr2EulerRotation
        pitchCurve:
            type: Tr2ScalarCurve
            length: 2
            cycle: 0
            timeScale: 1.0
            startValue: 0
            endValue: 1
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0"""
        actual = rot.__str__()
        self.assertEqual(expected, actual)

    def test_str_roll_curve(self):
        roll = red.Tr2ScalarCurve("rollCurve", 0.0, 2, 0, 1, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        rot = red.Tr2EulerRotation("MyObject", None, None, roll)
        expected = """
    - &euler_rotation_MyObject
        type: Tr2EulerRotation
        rollCurve:
            type: Tr2ScalarCurve
            length: 2
            cycle: 0
            timeScale: 1.0
            startValue: 0
            endValue: 1
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0"""
        actual = rot.__str__()
        self.assertEqual(expected, actual)

    def test_str_no_curve(self):
        rot = red.Tr2EulerRotation("MyRotation", None, None, None)
        expected = """
    - &euler_rotation_MyRotation
        type: Tr2EulerRotation"""
        actual = rot.__str__()
        self.assertEqual(expected, actual)

    def test_str_all_curves(self):
        yaw = red.Tr2ScalarCurve("yawCurve", 0.0, 0, 1, 2, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        pitch = red.Tr2ScalarCurve("pitchCurve", 0.0, 3, 4, 5, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        roll = red.Tr2ScalarCurve("rollCurve", 0.0, 6, 7, 8, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        rot = red.Tr2EulerRotation("MyObject", yaw, pitch, roll)
        expected = """
    - &euler_rotation_MyObject
        type: Tr2EulerRotation
        yawCurve:
            type: Tr2ScalarCurve
            length: 0
            cycle: 0
            timeScale: 1.0
            startValue: 1
            endValue: 2
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0
        pitchCurve:
            type: Tr2ScalarCurve
            length: 3
            cycle: 0
            timeScale: 1.0
            startValue: 4
            endValue: 5
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0
        rollCurve:
            type: Tr2ScalarCurve
            length: 6
            cycle: 0
            timeScale: 1.0
            startValue: 7
            endValue: 8
            startTangent: [3.0, 4.0, 3.0]
            endTangent: [5.0, 6.0, 5.0]
            interpolation: 2
            timeOffset: 0.0"""
        actual = rot.__str__()
        self.assertEqual(expected, actual)


class TestTr2VectorCurve(unittest.TestCase):
    def test_str(self):
        curve = red.Tr2VectorCurve("MyObject", 0.0, 1, 0, 1, [3.0, 4.0, 3.0], [5.0, 6.0, 5.0])
        expected = """
    - &location_curve_MyObject
        type: Tr2Vector3Curve
        name: "MyObject_location_curve"
        length: 1
        startValue: 0
        endValue: 1
        startTangent: [3.0, 4.0, 3.0]
        endTangent: [5.0, 6.0, 5.0]
        interpolation: 2
        timeOffset: 0.0"""
        actual = curve.__str__()
        self.assertEqual(expected, actual)

class TestTriCurveSet(unittest.TestCase):
    def test_str(self):
        curve_set = red.TriCurveSet("MyObject")
        expected = """
-   type: TriCurveSet
    name: "MyObject_curve_set"
    curves:"""
        actual = curve_set.__str__()
        self.assertEqual(expected, actual)

class TestEveSpaceScene(unittest.TestCase):
    def test_str(self):
        space_scene = red.EveSpaceScene()
        expected = """type: EveSpaceScene"""
        actual = space_scene.__str__()
        self.assertEqual(expected, actual)

    def test_one_curveset(self):
        space_scene = red.EveSpaceScene()
        curve_set = red.TriCurveSet("MyObject")
        space_scene.curve_sets.append(curve_set)
        expected = """type: EveSpaceScene
curveSets:
-   type: TriCurveSet
    name: "MyObject_curve_set"
    curves:"""
        actual = space_scene.__str__()
        self.assertEqual(expected, actual)