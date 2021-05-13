# fill config
import os
import sys
import shutil

local = False
user = 'wes'
accepted = ['-local', 'config/config.py','config.py', '-seth', '-wes']
for i in sys.argv:
    if i not in accepted:
        print(f'Error: \"{i}\" is not an accpeted arguement')
        print(f'accpted arguements are {accepted}')
        exit()

datasets = 'mnsit,cifar'
if '-local' in sys.argv:
    local = True
    datasets = ''


if '-seth' in sys.argv:
    user = 'seth'

if not local:
    os.mkdir('/root/.aws/')
    creds = '/content/drive/MyDrive/feature-attribution/config/'+user+'-credentials'
    shutil.copy(creds, '/root/.aws/credentials')
    shutil.copy('/content/drive/MyDrive/feature-attribution/config/config','/root/.aws/')


with open('config/config.txt', 'w') as f:
    f.write('user:%s\n' % (user))
    f.write('local:%s\n' % (str(local)))
    f.write('datasets:%s\n' % (datasets))