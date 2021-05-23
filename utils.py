# utils file

def get_model_list(model_dict, dataset='all'):
    list = []
    if dataset == 'all':
        for i in ['cifar', 'mnist', 'imagenet']:
            list+=model_dict[i]
    else:
        list = model_dict[dataset]

    return list


def make_string(input):
    if type(input) == str:
        return input
    elif type(input) == list:
        return ', '.join(input)
    elif type(input) == NoneType:
        return 'none'

def read_config():
    with open('config/config.txt', 'r') as f:
        config_dict = dict(line.strip().split(':') for line in f)

    if config_dict['local'] == 'False':
        config_dict['local'] = False
    elif config_dict['local'] == 'True':
        config_dict['local'] = True

    if config_dict['auto'] == 'False':
        config_dict['auto'] = False
    elif config_dict['auto'] == 'True':
        config_dict['auto'] = True

    return config_dict

def stren_input(input):
    if type(input) == dict:
        return input
