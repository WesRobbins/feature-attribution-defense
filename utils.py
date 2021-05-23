# utils file

def get_model_list(model_dict, dataset='all'):
    list = []
    if dataset == 'all':
        for i in ['cifar', 'mnist', 'imagenet']:
            list+=model_dict[i]
    else:
        list = model_dict[dataset]

    return list

def list_string(input):
    if type(input) == str:
        return input
    elif type(input) == list:
        return ', '.join(input)
        
