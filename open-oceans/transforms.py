import numpy as np

import torch
from torchvision import transforms


class RGBDataTransform:
    def __call__(self, data):
        return transforms.functional.to_tensor(data).float()