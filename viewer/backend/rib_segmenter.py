import numpy as np
import os
from skimage.transform import resize

from viewer.backend.trainable_models import get_u_net

# GET RID OF THIS
DEFAULT_WEIGHTS_PATH = "viewer/backend/trainable_models/weights/ribs_detection_u-net_22Jul2016_150.h5"


class RibSegmenter:
    def __init__(self, image_size=320, weights_filename=os.path.join(os.getcwd(), DEFAULT_WEIGHTS_PATH)):
        self.image_size = image_size
        self.model = get_u_net(image_size=image_size, do_lrn=False)
        self.model.compile(optimizer='adam', loss='binary_crossentropy')
        self.model.load_weights(weights_filename)

    def process(self, image):
        """
        Segments ribs on an X-ray image using CNN
        Postprocessing of CNN results is in progress
        :param image: 2d numpy array
        :return: 2d numpy array
        """
        resized = resize(image, [self.image_size, self.image_size])
        resized = (resized - resized.min()) * 255 / (resized.max() - resized.min())
        mask = self.model.predict(np.reshape(resized, (1, 1, self.image_size, self.image_size)))[0][0]
        mask_resized = resize(mask, [image.shape[0], image.shape[1]])
        processed = (mask_resized + 1) * image
        return processed
