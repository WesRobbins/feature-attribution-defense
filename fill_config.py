# fill config
import sys
local = False
user = 'wes'
accepted = ['-local', 'fill_config.py', '-seth', '-wes']
for i in sys.argv:
    if i not in accepted:
        print(f'Error: \"{i}\" is not an accpeted arguement')
        print(f'accpted arguements are {accepted}')
        exit()

if '-local' in sys.argv:
    local = True

if '-seth' in sys.argv:
    user = 'seth'



with open('config.txt', 'w') as f:
    f.write('user:%s\n' % (user))
    f.write('local:%s\n' % (str(local)))
    
