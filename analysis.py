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
