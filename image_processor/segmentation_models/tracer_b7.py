from typing import List, Tuple
from PIL.Image import Image as PILImage
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from tracer import TracerDecoder
from efficientnet import EfficientEncoderB7


class EmptyAutocast(object):
    """
    Empty class for disable any autocasting.
    """

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __call__(self, func):
        return


class TracerUniversalB7(TracerDecoder):
    name: str
    input_size: Tuple[int, int]
    model_path: str
    mean: List[float] = [0.485, 0.456, 0.406]
    std: List[float] = [0.229, 0.224, 0.225]
    device: str = "cpu"

    def __init__(self, model_path: str="path_to_model"):
        """
        Initialize the TRACER_B7 model
        """
        self.name = "tracer_b7_general"
        self.model_path = model_path
        self.input_size = (640, 640)
        super(TracerUniversalB7, self).__init__(
            encoder=EfficientEncoderB7(),
            rfb_channel=[32, 64, 128],
            features_channels=[48, 80, 224, 640],
        )
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize(self.input_size),
                transforms.Normalize(self.mean, self.std),
            ]
        )
        self.to(self.device)
        self.load_state_dict(
            torch.load(self.model_path, map_location=self.device), strict=False
        )
        self.eval()

    def data_preprocessing(self, data: PILImage) -> torch.FloatTensor:
        """
        Transform input image to suitable data format for neural network

        Args:
            data: input image

        Returns:
            input for neural network

        """

        return torch.unsqueeze(self.transform(data), 0).type(torch.FloatTensor)

    @staticmethod
    def data_postprocessing(
        data: torch.tensor, original_image: PILImage
    ) -> PILImage:
        """
        Transforms output data from neural network to suitable data
        format for using with other components of this framework.

        Args:
            data: output data from neural network
            original_image: input image which was used for predicted data

        Returns:
            Segmentation mask as PIL Image instance

        """
        output = (data.type(torch.FloatTensor).detach().cpu().numpy() * 255.0).astype(
            np.uint8
        )
        # output = output.squeeze(0)
        output = np.squeeze(output)
        mask = Image.fromarray(output).convert("L")
        mask = mask.resize(original_image.size, resample=Image.BILINEAR)
        return mask

    def inference(self, img: PILImage)-> PILImage:
        """
        Apply inference operations on each images(Preproccessing, )
        """
        pre_img = self.data_preprocessing(img)
        with torch.no_grad():
            pre_img = pre_img.to(self.device)
            mask = super(TracerDecoder, self).__call__(pre_img)
            mask_cpu = mask.cpu()
            del mask, pre_img
        mask = self.data_postprocessing(mask_cpu, img)
        return mask
