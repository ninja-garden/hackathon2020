import math
from PIL import Image
from typing import Dict

from .detector import Detector
from .util import print_err, RegistryRequester, pxl_to_geo, rotate_point2d

class Processor:
    def __init__(self, config: Dict[str, str]):
        if not 'detector_model' in config:
            print_err('Error: not found "detector_model" in config')
            exit(1)
        self.detector = Detector(config['detector_model'])

        self.registry = None
        if 'chrome_web_driver' in config:
            self.registry = RegistryRequester(selenium_driver_path=config['chrome_web_driver'])
        else:
            self.registry = RegistryRequester()

    def __call__(self, image: Image, north: float, south: float, west: float, east: float):
        buildings = self.detector.detect(image)
        bottom_pxl = image.size[1] - 1
        geo_to_pxl_ratio = (north - south) / image.size[1]
        result = []

        for building in buildings:
            x1, y1, x2, y2, theta = building

            # A little workaround with bottom pxl due to PIL's coordinate system starting at the top left corner.
            sx2, sy2 = rotate_point2d(x2, bottom_pxl - y2, -theta)

            cx, cy = (sx2 - x1) / 2, (sy2 - (bottom_pxl - y1)) / 2
            cx, cy = rotate(cx, cy, theta)
            lat, lon = south + pxl_to_geo(cy, geo_to_pxl_ratio), west + pxl_to_geo(cx, geo_to_pxl_ratio)

            info = self.registry(lat, lon)

            result.append({'x1': })
