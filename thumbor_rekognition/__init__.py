#!/usr/bin/env python

# standard library imports
from io import BytesIO

# third party related imports
import boto3
from thumbor.config import Config
from thumbor.detectors import BaseDetector
from thumbor.point import FocalPoint
from thumbor.utils import logger

# local library imports


Config.define(
    'REKOGNITION_REGION', 'us-east-1', 'AWS Rekognition service region'
)


class Detector(BaseDetector):

    def detect(self, callback):

        raw_bytes = self.read_jpeg_bytes()
        faces = self.detect_faces(raw_bytes)

        if len(faces) == 0:
            self.next(callback)
            return

        focal_points = [f.focal_point(*self.size()) for f in faces]
        self.context.request.focal_points.extend(focal_points)
        callback()

    def read_jpeg_bytes(self):
        """Convert input image to JPEG format

        AWS Rekognition only supports JPEG and PNG images. To make other
        image formats (e.g. webp) works, we normalize to JPEG image.

        """

        bio = BytesIO()
        self.context.modules.engine.image.save(bio, 'JPEG')
        return bio.getvalue()

    def size(self):

        return self.context.modules.engine.size

    def rekognition_client(self):

        return boto3.client(
            'rekognition',
            region_name=self.context.config.get('REKOGNITION_REGION')
        )

    def detect_faces(self, raw_bytes):

        try:
            resp = self.rekognition_client().detect_faces(
                Image={'Bytes': raw_bytes},
                Attributes=['DEFAULT']
            )
            return [Face(fd) for fd in resp.get('FaceDetails', [])]

        except Exception as e:
            logger.exception(e)
            return []


class Face(object):
    """AWS Rekognition API response wrapper"""

    def __init__(self, api_resp):

        self.api_resp = api_resp

    def focal_point(self, overall_width, overall_height):

        bbox = self.api_resp['BoundingBox']
        x = int(bbox['Left'] * overall_width)
        y = int(bbox['Top'] * overall_height)
        w = int(bbox['Width'] * overall_width)
        h = int(bbox['Height'] * overall_height)

        return FocalPoint.from_square(x, y, w, h, origin='RekognitionDetector')

