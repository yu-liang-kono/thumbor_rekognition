#!/usr/bin/env python

# standard library imports
import imghdr
import os.path
from unittest import TestCase

# third party related imports
from mock import MagicMock
from mock import call, patch
from PIL import Image
from thumbor.config import Config

# local library imports
from thumbor_rekognition import Detector, Face


class TestReadJpegBytes(TestCase):

    def setUp(self):

        ctx = MagicMock()
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        png = os.path.join(curr_dir, 'fixtures', 'smallest.png')

        ctx.modules.engine.image = Image.open(png)
        self.detector = Detector(ctx, 0, [])

    def test(self):

        raw_bytes = self.detector.read_jpeg_bytes()
        self.assertEqual(imghdr.what(None, raw_bytes), 'jpeg')


class TestSize(TestCase):

    def test(self):

        ctx = MagicMock()
        ctx.modules.engine.size = (1, 1)
        detector = Detector(ctx, 0, [])
        self.assertEqual(detector.size(), (1, 1))


class TestRekognitionClient(TestCase):

    @patch('thumbor_rekognition.boto3')
    def test(self, mock_boto3):

        ctx = MagicMock()
        ctx.config = Config(REKOGNITION_REGION='r')

        mock_boto3.client.return_value = mock_client = MagicMock()
        detector = Detector(ctx, 0, [])

        self.assertEqual(detector.rekognition_client(), mock_client)
        mock_boto3.client.assert_called_with('rekognition', region_name='r')


class TestDetectFaces(TestCase):

    def test(self):

        ctx = MagicMock()
        detector = Detector(ctx, 0, [])

        mock_client = MagicMock()
        detector.rekognition_client = MagicMock(return_value=mock_client)
        mock_client.detect_faces.return_value = {'FaceDetails': [True]}

        faces = detector.detect_faces('')

        self.assertIsInstance(faces[0], Face)
        mock_client.detect_faces.assert_called_with(
            Image={'Bytes': ''}, Attributes=['DEFAULT']
        )


class TestDetect(TestCase):

    def setUp(self):

        ctx = MagicMock()
        ctx.request.focal_points = []

        self.detector = Detector(ctx, 0, [])
        self.mock_detector_methods()

    def mock_detector_methods(self):

        self.detector.read_jpeg_bytes = MagicMock(return_value='')
        self.detector.detect_faces = MagicMock(return_value=[])
        self.detector.next = MagicMock()
        self.detector.size = MagicMock(return_value=(1, 1))

    def test_when_no_face_is_found(self):

        callback = True
        self.detector.detect_faces = MagicMock(return_value=[])
        self.detector.detect(callback)

        self.detector.read_jpeg_bytes.assert_called_with()
        self.detector.detect_faces.assert_called_with('')
        self.detector.next.assert_called_with(callback)

    def test_when_face_is_found(self):

        mock_callback = MagicMock()

        mock_face = MagicMock()
        mock_face.focal_point.return_value = True
        self.detector.detect_faces = MagicMock(return_value=[mock_face])

        self.detector.detect(mock_callback)

        self.detector.read_jpeg_bytes.assert_called_with()
        self.detector.detect_faces.assert_called_with('')
        self.detector.size.assert_called_with()

        mock_face.focal_point.assert_called_with(1, 1)
        self.assertIn(True, self.detector.context.request.focal_points)
        self.assertTrue(mock_callback.called)

