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

def get_tuple(attack, defense, strens=True, steps=False):
    models = ['vgg11_bn', 'vgg13_bn', 'vgg16_bn', 'vgg19_bn', 'densenet121', 'densenet161',
            'densenet169', 'googlenet', 'inception_v3', 'mobilenet_v2', 'resnet18', 'resnet34',
            'resnet50']
    attack_strens = ['0.001', '0.003', '0.01', '0.03', '0.07', '0.1', '0.2', '0.3']
    steps_list = [10]
    tuples = []

    for m in models:
        if steps and strens:
            for a in attack_strens:
                for s in steps_list:
                    tuples.append((m, a, s))
        elif strens:
            for a in attack_strens:
                tuples.append((m, a))
        elif steps:
            for s in steps_list:
                tuples.append((m, s))



    return tuples

def get_stren(stren_dict):
    for i in range(len(stren_dict)):
        if 'eps' and 'steps' in stren_dict[i].keys():
            stren_dict[i] = stren_dict[i]['eps']+str(stren_dict[i]['steps'])
        elif 'eps' in stren_dict[i].keys():
            stren_dict[i] = stren_dict[i]['eps']
        elif 'steps' in stren_dict[i].keys():
            stren_dict[i] = str(stren_dict[i]['steps'])
        else:
            stren_dict[i] = ''

    return stren_dict





""" returns results that match parameters
    - params can be lists or single string
    - models are required               """
def get_results(results, id=None, models=None, attacks='none', defenses='none',
        dataset='cifar', attack_strengths=None):

    if type(attack_strengths) == float:
        attack_strengths = [attack_strengths]

    vals = []
    for i in results:
        if id:
            if int(i.id) not in id:
                continue
        if attack_strengths: # TODO
            if type(i.attack_strength) == str:
                continue
            elif i.attack_strength not in attack_strengths:
                continue
        if i.model not in models:
            continue
        if i.attack not in attacks:
            continue
        if i.defense not in defenses:
            continue
        if i.dataset not in dataset:
            continue
        vals.append(i)

    return vals

def axis_arrays(results, axis='attack_strength', metric='accuracy'):
    axises = ['model', 'attack', 'defense', 'dataset', 'attack_strength']
    assert axis in axises

    axises.remove(axis)
    vals = {}
    for i in results:
        i = i.get_dict()
        li = []
        for ax in axises:
            li.append(i[ax])
        li = tuple(li)
        if li not in vals.keys():
            vals[li] = []
        vals[li].append((i[axis], i[metric]))

    return vals
