# plots based on data
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_theme(style="whitegrid")

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
    print(df)

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