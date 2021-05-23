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
