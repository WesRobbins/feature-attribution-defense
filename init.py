# library imports
import shutil
import os
import sys
import git
# repo file imports
from settings import current_settings
import database
from datasets import data


""" global vars """
database = database.Database()
results = []

""" path set up """
sys.path.insert(1, '/content/cifar-pytorch/cifar10_models')
