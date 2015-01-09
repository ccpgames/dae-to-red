import unittest
import colladamunge
import StringIO

import example_data


def get_animations_ripped_from_test_file():
    collada_instance = colladamunge.get_collada_instance_for_file(StringIO.StringIO(example_data.test_file))
    return colladamunge.rip_animations_from_collada_instance(collada_instance)


class TestColladamunge(unittest.TestCase):

    def testRipAnimationsFromFileReturnsCorrectNumberOfAnimations(self):
        animations = get_animations_ripped_from_test_file()
        actual = len(animations)
        self.assertEqual(1, actual)

    def testSourcesGetExtracted(self):
        self.maxDiff = None
        expected = example_data.get_sources()
        animations = get_animations_ripped_from_test_file()
        actual = animations[0].sources
        self.assertEqual(expected, actual)

    def testChannelsGetExtracted(self):
        expected = example_data.get_channels()
        animations = get_animations_ripped_from_test_file()
        actual = animations[0].channels
        self.assertEqual(expected, actual)

    def testSamplersGetExtracted(self):
        expected = example_data.get_samplers()
        animations = get_animations_ripped_from_test_file()
        actual = animations[0].samplers
        self.assertEqual(expected, actual)

    def testAnimationsGetExtracted(self):
        expected = example_data.get_animations()
        animations = get_animations_ripped_from_test_file()
        actual = animations[0].animations
        self.assertEqual(expected, actual)

    def testRipAnimationsFromFile(self):
        sources = example_data.get_sources()
        channels = example_data.get_channels()
        samplers = example_data.get_samplers()
        example_animations = example_data.get_animations()

        animations = get_animations_ripped_from_test_file()

        expected = colladamunge.Animation(sources, channels, samplers, example_animations)
        actual = animations[0]

        self.assertEqual(expected, actual)
