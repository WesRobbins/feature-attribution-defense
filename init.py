# library imports
import shutil
import os
import sys
import importlib
from importlib import reload

# repo file imports
from settings import current_settings
import database
from datasets import data
from resultsgraphs import *

# colab only imports
if not current_settings.local:
    import torchattacks


""" path set up """
if not current_settings.local:
    sys.path.insert(1, '/content/cifar-pytorch/cifar10_models/')
    sys.path.insert(1, '/content/feature-attribution-defense/models/')
    # sys.path.insert(1, '/content/art-git/')
    # sys.path.insert(1, '/content/adver_torch/torchattacks/')
if current_settings.local:
    sys.path.insert(1, '/Users/wesrobbins/Desktop/cp/research-repos/feature-attribution-defense')

""" sets of models """
model_set_names = {
        'all_models':
                    {
                    'cifar':
                        ['vgg11_bn', 'vgg13_bn', 'vgg16_bn', 'vgg19_bn', 'densenet121', 'densenet161',
                        'densenet169', 'googlenet', 'inception_v3', 'mobilenet_v2', 'resnet18', 'resnet34',
                        'resnet50'],
                    'mnist:':
                        [],
                    'imagenet':
                        [],
                    },
        'no_models':
                    {
                    'cifar': [],
                    'mnist:': [],
                    'imagenet': []
                    }
}

""" global vars """
db = database.Database()
results = db.load_all(model_set_names)

if not current_settings.local:
    import load_models
    from load_models import load_models
    from load_models import device

    loaded_models = load_models(model_set_names[current_settings.model_set])


current_settings.print_settings()
