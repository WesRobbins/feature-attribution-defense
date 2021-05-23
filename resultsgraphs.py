# plots based on data
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import result
from result import get_results, axis_arrays
from utils import *
from analysis import *

sns.set_theme(style="whitegrid")
# sns.set(rc={'figure.figsize':(11.7,8.27)})

def model_bar_graph(results, attack='none', defense='none', metric='acc', dataset='cifar'):
    new = []
    for i in results:
        if i.attack == attack and i.defense == defense:
            new.append(i)

    acc = []
    loss = []
    names = []
    for i in new:
        acc.append(i.accuracy)
        loss.append(i.loss)
        name = i.model[i.model.find('-')+1:]
        names.append(name)

    if metric == 'acc':
        data = acc
    elif metric == 'loss':
        data = loss
    df = pd.DataFrame(list(zip(names, data)), columns =['Name', metric])


    ax = sns.barplot(x="Name", y=metric, data=df)

    subtitle_string = "Dataset: " + dataset + "      Attack: " +attack+ "      Defense: " + defense
    plt.title(subtitle_string, fontsize=10, fontweight="bold")
    plt.suptitle("Model Performance", y=.99, fontsize=18)

    even = True
    for tick in ax.xaxis.get_major_ticks():
        if not even:
            tick.set_pad(15)
        even = not even
        tick.label.set_fontsize(10)

    plt.xlabel('model architecture', fontsize=16)
    plt.ylabel(metric, fontsize=16)

    plt.show()

def defense_bar_graph(results, model, attack='none', defense='none', metric='acc', dataset='cifar'):
    new = []
    for i in results:
        if i.attack == attack and i.defense == defense:
            new.append(i)

    acc = []
    loss = []
    names = []
    for i in new:
        acc.append(i.accuracy)
        loss.append(i.loss)
        name = i.model[i.model.find('-')+1:]
        names.append(name)

    if metric == 'acc':
        data = acc
    elif metric == 'loss':
        data = loss
    df = pd.DataFrame(list(zip(names, data)), columns =['Name', metric])
    ax = sns.barplot(x="Name", y=metric, data=df)

    subtitle_string = "Dataset: " + dataset + "      Attack: " +attack+ "      Defense: " + defense
    plt.title(subtitle_string, fontsize=10, fontweight="bold")
    plt.suptitle("Model Performance", y=.99, fontsize=18)

    even = True
    for tick in ax.xaxis.get_major_ticks():
        if not even:
            tick.set_pad(15)
        even = not even
        tick.label.set_fontsize(10)

    plt.xlabel('model architecture', fontsize=16)
    plt.ylabel(metric, fontsize=16)

    plt.show()

def attack_stren_line_graph(results, models, attacks='none',
        defenses='none', metric='accuracy', dataset='cifar'):


    data = axis_arrays(get_results(results, models=models, attacks=attacks,
            defenses=defenses, dataset=dataset))

    for key in data.keys():
        data[key].sort(key=lambda x: x[0])
        data[key] = [x[1] for x in data[key]]



    data = pd.DataFrame.from_dict(data)
    data = pd.DataFrame.from_records(data, index=[.001,.01,.05,.1,.2,.3])
    print(data)

    subtitle_string = "Dataset: " + list_string(dataset) + "      Attack: " + list_string(attacks)+ "      Defense: " + list_string(defenses)
    plt.title(subtitle_string, fontsize=10, fontweight="bold")
    plt.suptitle("Model Performance", y=.99, fontsize=18)
    plt.xlabel('attack strength')
    plt.ylabel('acc')
    sns.lineplot(data=data)
    plt.show()

def l2_acc_graph(results, models, attacks='fgsm', defenses='none', dataset='cifar', attack_strengths=.1):
    pass
