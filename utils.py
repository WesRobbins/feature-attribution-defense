# utils file

def get_model_list(model_dict, dataset='all'):
    list = []
    if dataset == 'all':
        for i in ['cifar', 'mnist', 'imagenet']:
            list+=model_dict[i]
    else:
        list = model_dict[dataset]

    return list
