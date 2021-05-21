# fill config
import os
import sys
import shutil


local = False
user = 'wes'
accepted = ['-local', 'config/config.py','config.py', '-seth', '-wes',
            '-cmi', '-cm', '-mi', '-ci', '-c', '-m', '-i']

for i in sys.argv:
    if i not in accepted:
        print(f'Error: \"{i}\" is not an accpeted arguement')
        print(f'accpted arguements are {accepted}')
        exit()
datasets = 'mnist,cifar'
if '-c' in sys.argv:
    datasets = 'cifar'
elif '-m' in sys.argv:
    datasets = 'mnists'
elif '-i' in sys.argv:
    datasets = 'imagenet'
elif '-cmi' in sys.argv:
    datasets = 'cifar,mnist,imagenet'
    
model_set = 'all_models'

if '-local' in sys.argv:
    local = True
    datasets = ''
    model_set = 'no_models'


if '-seth' in sys.argv:
    user = 'seth'

if not local:
    os.mkdir('/root/.aws/')
    creds = '/content/drive/MyDrive/feature-attribution/config/'+user+'-credentials.txt'
    shutil.copy(creds, '/root/.aws/credentials')
    shutil.copy('/content/drive/MyDrive/feature-attribution/config/config','/root/.aws/')

    from git import Repo

    Repo.clone_from('https://github.com/huyvnphan/PyTorch_CIFAR10', '/content/cifar-pytorch')




with open('config/config.txt', 'w') as f:
    f.write('user:%s\n' % (user))
    f.write('local:%s\n' % (str(local)))
    f.write('datasets:%s\n' % (datasets))
    f.write('model_set:%s\n' % (model_set))
