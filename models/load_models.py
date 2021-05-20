# load models into runtime

import torch
import sys
import os

from vgg import vgg11_bn, vgg13_bn, vgg16_bn, vgg19_bn
from densenet import densenet121, densenet161, densenet169
from googlenet import googlenet
from inception import inception_v3
from mobilenetv2 import mobilenet_v2
from resnet import resnet18, resnet34, resnet50
from resnet_orig import resnet_orig

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_models(names):
  print("\n LOADING Models")
  loaded_nets = {}
  for dataset in names:
      print(dataset + ':')
      for name in names[dataset]:
        print(name+'..', end='')
        net = get_net(name)
        # net = torch.nn.DataParallel(net)
        assert os.path.isfile('/content/drive/MyDrive/feature-attribution/torch-models/checkpoints/'+dataset+'/state_dicts/'+name+'.pt'), 'Error: no checkpoint directory found!'
        checkpoint = torch.load('/content/drive/MyDrive/feature-attribution/torch-models/checkpoints/'+dataset+'/state_dicts/'+name+'.pt')
        net.load_state_dict(checkpoint)
        m_name = dataset + '-' + name
        loaded_nets[m_name]=net
    # best_acc = checkpoint['acc']
    # start_epoch = checkpoint['epoch']
    # sp = ' '*(12-len(name))
    # print(f'{name}{sp}   Epoch: {start_epoch} Acc: {best_acc}')
  print()
  return loaded_nets


def get_net(name):
    if name == 'densenet121':
        net = densenet121()
    elif name == 'densenet161':
        net = densenet161()
    elif name == 'densenet169':
        net == densenet169()
    elif name == 'googlenet':
        net = googlenet()
    elif name == 'inception_v3':
        net = inception_v3()
    elif name == 'mobilenet_v2':
        net = mobilenet_v2()
    elif name == 'resnet18':
        net = resnet18()
    elif name == 'resnet34':
        net = resnet34()
    elif name == 'resnet50':
        net = resnet50()
    elif name == 'resnet_orig':
        net = resnet_orig()
    elif name == 'vgg11_bn':
        net = vgg11_bn()
    elif name == 'vgg13_bn':
        net = vgg13_bn()
    elif name == 'vgg16_bn':
        net = vgg16_bn()
    elif name == 'vgg19_bn':
        net = vgg19_bn()
    else:
        print(f'{name} not a valid model name')
        sys.exit(0)

    return net.to(device)
