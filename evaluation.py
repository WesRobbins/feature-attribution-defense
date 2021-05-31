import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn

import torchattacks

from settings import current_settings
from datasets import data

import progressbar

device = 'cuda' if torch.cuda.is_available() else 'cpu'


widgets = [progressbar.Percentage(), progressbar.Bar(), progressbar.ETA()]

def full_run(db, atk_names, models, attack_strenghts, defense=None, dataset='cifar'):
    for atck in att:
        for model in models:
            for stren in eps:
                eval_and_write(db, model, atck, defense, stren, dataset)

def eval_and_write(db, net_name, atk=None, defense=None, eps=None, dataset='cifar'):

    results = evaluation_loop(net_name, dataset, atk=atk, defense=defense,
                              eps=eps)
    if not atk:
      atk = 'none'
    if not defense:
      defense = 'none'
    if not eps:
      eps = 'n/a'

    db.write(atk=atk, defense=defense, eps=eps,
                          model=net_name, dataset=dataset, accuracy=results[0], loss=results[1], l2=results[2])

# returns loss, accuracy
def evaluation_loop(net_name, dataset, epoch=None, atk=None, defense=None, eps=None):
    net = current_settings.loaded_models[dataset][net_name]
    ds_name = dataset + '_tl'
    testloader = data[ds_name]
    criterion = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    net.eval()
    test_loss = 0
    correct = 0
    total = 0
    l2 = 'n/a'
    if atk:
      # cont = nullcontext()
      l2 = 0
      atck = get_atk(net, atk, eps)
    else:
      # cont = torch.no_grad()
      pass

    if defense:
      pass


    # with cont:
    if atk: bar = progressbar.ProgressBar(max_value=len(testloader), widgets=widgets)
    for batch_idx, (inputs, targets) in enumerate(testloader):
        inputs, targets = inputs.to(device), targets.to(device)

        if atk:
          atck_inputs = atck(inputs, targets)
          l2+= mse(inputs, atck_inputs).item()
          inputs = atck_inputs
        outputs = net(inputs)
        loss = criterion(outputs, targets)
        test_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        if atk: bar.update(batch_idx)

    if atk:
      bar.finish()
      print(f'{atk} atk')
      l2 = l2/len(testloader)

    loss = test_loss/len(testloader)
    acc = 100.*correct/total
    print(f'Model: {net_name}   Attack: {atk}    Defense: {defense}  Dataset: {dataset}')
    print(f'METRICS - Loss: {loss:.3f} | Acc: {acc:.3f} {correct}/{total} | l2: {l2}')



    return acc, loss, l2


def get_atk(model, atk_name, eps):

    eps = float(eps['eps'])

    if atk_name == 'fgsm':
        return torchattacks.FGSM(model, eps=eps)
    elif atk_name == 'bim':
        return torchattacks.BIM(model, eps=eps, steps=steps, alpha=eps/(steps*.5))
    elif atk_name == 'deepfool':
        return torchattacks.DeepFool(model, steps=steps)
    elif atk_name == 'cw':
        return torchattacks.CW(model)
    elif atk_name == 'pgd':
        return torchattacks.PGD(model, eps=eps, steps=steps, alpha=eps/(steps*.5))
    elif atk_name == 'rfgsm':
        return torchattacks.RFGSM(model, eps=eps, alpha=eps)
    elif atk_name == 'auto-attack':
        return torchattacks.AutoAttack(model, eps=eps)
    elif atk_name == 'mifgsm':
        return torchattacks.MIFGSM(model, eps=eps, steps=steps)
    elif atk_name == 'square':
        return torchattacks.Square(model, eps=eps)
    elif atk_name == 'fab':
        return torchattacks.FAB(model, eps=eps)
    elif atk_name == 'one-pixel':
        return torchattacks.OnePixel(model)
    elif atk_name == 'gn':
        return torchattacks.GN(model, sigma=eps)
    elif atk_name == 'apgd':
        return torchattacks.APGD(model, eps=eps)
    elif atk_name == 'eotpgd':
        return torchattacks.EOTPGD(model, eps=eps, steps=steps, alpha=eps/(steps*.5))
    elif atk_name == 'pgddlr':
        return torchattacks.PGDDLR(model, eps=eps, steps=steps, alpha=eps/(steps*.5))
    elif atk_name == 'ffgsm':
        return torchattacks.FFGSM(model, eps=eps, alpha=eps)
    elif atk_name == 'sparsefool':
        return torchattacks.SparseFool(model)

    else:
        print("Attack not valid")
        sys.exit(-1)


def get_defense():
  pass
