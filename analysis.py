# functions to analyze results
from result import *
def l2_acc(results, models, attacks='fgsm', defenses='none', dataset='cifar', attack_strengths=.1):
    re = get_results(results, models=models, attacks=attacks, defenses=defenses,
            dataset=dataset, attack_strengths=attack_strengths)
    base = get_results(results, models=models, dataset=dataset)


    vals = {}
    for i in re:
        key = (i.model, i.attack, i.defense, i.dataset, i.attack_strength)
        base_re = None
        for j in base:
            if i.model == j.model and i.dataset == j.dataset:
                base_re = j.accuracy

        vals[key] = (base_re-i.accuracy) / i.l2

    return vals

def avg_acc(results, models, attacks='fgsm', defenses='none', dataset='cifar', attack_strengths=.1):
    re = get_results(results, models=models, attacks=attacks, defenses=defenses,
            dataset=dataset, attack_strengths=attack_strengths)
    acc = 0
    for i in re:
        acc +=i.accuracy

    return acc/len(re)

def avg_l2_acc_ratio(results, models, attacks='fgsm', defenses='none', dataset='cifar', attack_strengths=.1):
    vals = l2_acc(results, models, attacks, defenses, dataset, attack_strengths)
    ratio = 0
    for i in vals.values():
        ratio += i

    return ratio/len(x)


# avgs dict hierarchy
#           avgs
#   full    partial     quick
#       loss   acc
#   all]    detailed
# det:by_attack det:by_model det: by_dataset

# enumerated hierarchy
#
# avgs
#   Loss
#       all
#       detailed
#           by_attack
#               all
#               by_stren
#           by_model
#                all
#           by_dataset
#               all
#   Acc
#       detailed
#           by_attack
#               all
#               by_stren
#           by_model
#           by_dataset



class Full_Analysis:
    def __init__(self, results, defense=None):
        self.defense = defense
        self.results = self.get_results(results, defense)
        self.sets = self.available_results()
        self.avgs = self.get_avgs()
        self.detail_set = get_detail_set()

    def get_avgs(self):
        avgs = {'full':{}, 'partial':{}, 'quick':{}}
        for i in avgs.keys():
            avgs[i]['acc'] = {}
            avgs[i]['acc']['all'] = self.get_metric_avg('accuracy', self.sets[i])
            avgs[i]['acc']['detailed'] = self.detailed_avgs('accuracy', self.sets[i])

            avgs[i]['loss'] = {}
            avgs[i]['loss']['all'] = self.get_metric_avg('loss', self.sets[i])
            avgs[i]['loss']['detailed'] = self.detailed_avgs('loss', self.sets[i])


        return avgs


    def get_metric_avg(self, metric, set):
        total = 0
        if not set:
            return False
        for i in set:
            dict = i.get_dict()
            total += dict[metric]

        return total/len(set)

    def detailed_avgs(self, metric, set):
        detailed = {}
        detailed['by_attack'] = get_detailed(metric, set, 'attack')
        detailed['by_model'] = get_detailed(metric, set, 'model')
        detailed['by_dataset'] = get_detailed(metric, set, 'dataset')

        return detailed

    def get_detailed(self, metric, set, detail):
        detailed = {}
        detailed['all'] = get_detailed_val(metric, set, detail)

    def get_detail_val(self, metric, set, detail):
        total = 0
        if not set:
            return False
        for i in set:
            dict = i.get_dict()
            # TODO 
            if i[detail] == False:
                total += dict[metric]

        return total/len(set)
    def get_detailed2(self, metric, set, detail, detail2):
        pass

    def get_results(self, results, defense):
        if not defense:
            return self.get_results(results, 'none')
        re = []
        for i in results:
            if i.defense == defense:
                re.append(i)
        return re

    def available_results(self):
        re = {'full':[], 'partial':False, 'quick':False}
        re['full'] = self.results

        return re

    def get_detail_set(self):
        set = {
        'quick': {
            'attack': [],
            'model' : [],
            'dataset' : []
        },
        'partial': {
            'attack': [],
            'model' : [],
            'dataset' : []
        },
        'full': {
            'attack':
                ['fgsm', 'bim', 'deepfool', 'cw', 'pgd', 'rfgsm', 'auto-attack', 'mifgsm',
               'square', 'fab', 'one-pixel', 'gn', 'apgd', 'eotpgd', 'pgddlr', 'ffgsm',
               'sparsefool'],
            'model':
                ['vgg11_bn', 'vgg13_bn', 'vgg16_bn', 'vgg19_bn', 'densenet121', 'densenet161',
                'densenet169', 'googlenet', 'inception_v3', 'mobilenet_v2', 'resnet18', 'resnet34',
                'resnet50'],
            'dataset':
                ['cifar', 'mnist', 'imagent'],
        }
        }
