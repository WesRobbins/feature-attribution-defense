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
from result import *
from utils import *
from analysis import *
# colab only imports
if not current_settings.local:
    import torchattacks
    from evaluation import *


""" path set up """
if not current_settings.local:
    sys.path.insert(1, '/content/cifar-pytorch/cifar10_models/')
    sys.path.insert(1, '/content/feature-attribution-defense/models/')

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
                    'mnist':
                        [],
                    'imagenet':
                        [],
                    },
        'no_models':
                    {
                    'cifar': [],
                    'mnist': [],
                    'imagenet': []
                    }
}


# model_list = get_model_list(model_set_names[current_settings.model_set])
model_list = get_model_list(model_set_names['all_models'])

""" global vars """
db = database.Database()
results = db.load_all()

attack_strens = [.001, .003, .01, .03, .07, .1, .2, .3]

if not current_settings.local:
    import load_models
    from load_models import load_models
    from load_models import device

    current_settings.loaded_models = load_models(model_set_names[current_settings.model_set])
    loaded_model = current_settings.loaded_models


current_settings.print_settings()

config = read_config()
if config['auto']:
    pass
