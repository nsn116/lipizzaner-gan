from torch.autograd import Variable
from torchvision import datasets
from data.data_loader import DataLoader

from torchvision.utils import save_image
from torchvision.transforms import transforms
from helpers.pytorch_helpers import denorm

class MNISTDataLoader(DataLoader):

    def __init__(self, use_batch=True, batch_size=100, n_batches=0, shuffle=False):
        super().__init__(datasets.MNIST, use_batch, batch_size, n_batches, shuffle)

    @property
    def n_input_neurons(self):
        return 784

    @property
    def num_classes(self):
        return 10

    def transform(self):
        if self.cc.settings['network']['name'] == 'ssgan_convolutional_mnist':
            return transforms.Compose(
                [
                    transforms.Resize(64),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        (0.5, 0.5, 0.5),
                        (0.5, 0.5, 0.5)
                    )
                 ]
            )
        else:
            return super().transform()

    def save_images(self, images, shape, filename):
        if self.cc.settings['network']['name'] == 'ssgan_convolutional_mnist':
            import logging
            _logger = logging.getLogger(__name__)
            _logger.info(images)
            _logger.info(images.shape)
            data = images.data if isinstance(images, Variable) else images
            _logger.info(data.shape)
            save_image(denorm(data), filename)
        else:
            super().save_images(images, shape, filename)

    def transpose_data(self, data):
        if self.cc.settings['network']['name'] == 'ssgan_convolutional_mnist':
            return data
        else:
            return super().transpose_data(data)
