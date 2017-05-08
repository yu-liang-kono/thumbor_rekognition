#!/usr/bin/env python

# standard library imports
from unittest import TestCase

# third party related imports

# local library imports
from thumbor_rekognition import Face


class TestFocalPoint(TestCase):

    def test(self):

        resp = {
            "BoundingBox": {
                "Height": 0.09666666388511658,
                "Left": 0.32405567169189453,
                "Top": 0.04333333298563957,
                "Width": 0.1729622334241867
            }
        }
        face = Face(resp)
        focal_point = face.focal_point(885, 1582)

        self.assertEqual(focal_point.x, 362)
        self.assertEqual(focal_point.y, 144)
        self.assertEqual(focal_point.width, 153)
        self.assertEqual(focal_point.height, 152)
        self.assertEqual(focal_point.origin, 'RekognitionDetector')
