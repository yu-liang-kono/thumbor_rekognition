# thumbor_rekognition
Enable thumbor to use AWS rekognition to run face detection

[![Build Status](https://travis-ci.org/yu-liang-kono/thumbor_rekognition.svg?branch=master)](https://travis-ci.org/yu-liang-kono/thumbor_rekognition)
[![Coverage Status](https://coveralls.io/repos/github/yu-liang-kono/thumbor_rekognition/badge.svg?branch=master)](https://coveralls.io/github/yu-liang-kono/thumbor_rekognition?branch=master)
[![PyPI version](https://badge.fury.io/py/thumbor_rekognition.svg)](https://badge.fury.io/py/thumbor_rekognition)

[thumbor](https://github.com/thumbor/thumbor) is a smart imaging service. It enables on-demand crop, resizing and flipping of images. It also features a smart detection of important points in the image for better cropping and resizing, using opencv face detection algorithms.

[AWS Rekognition](http://docs.aws.amazon.com/rekognition/latest/dg/what-is.html) can quickly detect faces in image using sophisticated deep learning-based visual search and image classification.

thumbor_rekognition helps to use AWS Rekognition service to do face detection in thumbor easily.

## Installation

```bash
pip install thumbor_rekognition
```
    
## Enable detector
Add `thumbor_rekognition` to your `thumbor.conf`. Do not include thumbor's out-of-box face detector.

```python
DETECTORS = [
    # Do not use out-of-box face detector
    # 'thumbor.detectors.face_detector',

    # Include thumbor_rekognition
    'thumbor_rekognition',
    'thumbor.detectors.feature_detector',
]
```

The above configuration tells thumbor that it should run both the facial detection and the feature detection. These are mutually exclusive, meaning that if a face is detected, the feature detector won’t be run.

## AWS Rekognition
### Authentication
Authentication is handled by botocore, see [Boto3 documentation](https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration).

### Region
To set the region to use Rekognition service, add `REKOGNITION_REGION` to your `thumbor.conf`. Default is `us-east-1`.

```python
# AWS region for the Rekognition service
REKOGNITION_REGION = 'us-west-2'
```

## Using it
After installing thumbor_rekognition, you can test it by using the following URL.
```
http://<thumbor>:<port>/unsafe/300x300/smart/my.domain.com/picture.png
```

If you need to see what thumbor is seeing in your image, prepend `/debug` to all the parameters.
```
http://<thumbor>:<port>/unsafe/debug/300x300/smart/my.domain.com/picture.png
```
