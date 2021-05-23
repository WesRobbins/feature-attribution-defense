import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn

import progressbar
widgets = [progressbar.Percentage(), progressbar.Bar()]

def full_run(db, attack_names, models, attack_strenghts, defense=None, dataset='cifar'):
    for atck in att:
        for model in models:
            for stren in attack_strengths:
                eval_and_write(db, model, atck, defense, stren, dataset)

def fastest_run(db, defense, model='vgg19_bn', dataset='cifar'):
    attacks = ['fgsm', 'cw']
    for atck in attacks:
        eval_and_write(db, model, atck, defense, stren, dataset)

def eval_and_write(db, net_name, attack=None, defense=None, attack_strength=None, dataset='cifar'):

    results = evaluation_loop(net_name, dataset, attack=attack, defense=defense,
                              attack_strength=attack_strength)
    if not attack:
      attack = 'none'
    if not defense:
      defense = 'none'
    if not attack_strength:
      attack_strength = 'n/a'

    db.write_result(attack=attack, defense=defense, attack_strength=attack_strength,
                          model=net_name, dataset=dataset, accuracy=results[0], loss=results[1], l2=results[2])

# returns loss, accuracy
def evaluation_loop(net_name, dataset, epoch=None, attack=None, defense=None, attack_strength=None):
    net = loaded_models[dataset][net_name]
    ds_name = dataset + '_tl'
    testloader = data[ds_name]
    criterion = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    net.eval()
    test_loss = 0
    correct = 0
    total = 0
    l2 = 'n/a'
    if attack:
      # cont = nullcontext()
      l2 = 0
      atck = get_attack(net, attack, attack_strength)
    else:
      # cont = torch.no_grad()
      pass

    if defense:
      pass


    # with cont:
    if attack: bar = progressbar.ProgressBar(max_value=len(testloader), widgets=widgets)
    for batch_idx, (inputs, targets) in enumerate(testloader):
        inputs, targets = inputs.to(device), targets.to(device)

        if attack:
          atck_inputs = atck(inputs, targets)
          l2+= mse(inputs, atck_inputs).item()
          inputs = atck_inputs
        outputs = net(inputs)
        loss = criterion(outputs, targets)
        test_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        if attack: bar.update(batch_idx)

    if attack:
      bar.finish()
      print(f'{attack} attack')
      l2 = l2/len(testloader)

    loss = test_loss/len(testloader)
    acc = 100.*correct/total
    print(f'Model: {net_name}   Attack: {attack}    Defense: {defense}  Dataset: {dataset}')
    print(f'METRICS - Loss: {loss:.3f} | Acc: {acc:.3f} {correct}/{total} | l2: {l2}')



    return acc, loss, l2


def get_attack(model, attack_name, attack_strength):
    if 'eps' in attack_strength.keys():
        eps = float(attack_strength['eps'])
    else:
        eps = None
    if 'steps' in attack_strength.keys():
        steps = float(attack_strength['steps'])
    else:
        steps = None
    if attack_name == 'fgsm':
        return torchattacks.FGSM(model, eps=attack_strength)
    elif attack_name == 'bim':
        return torchattacks.BIM(model, eps=attack_strength, steps=steps, alpha=attack_strength/(steps*.5))
    elif attack_name == 'deepfool':
        return torchattacks.DeepFool(model)
    elif attack_name == 'cw':
        return torchattacks.CW(model)
    elif attack_name == 'pgd':
        return torchattacks.PGD(model, eps=attack_strength, steps=steps, alpha=attack_strength/(steps*.5))
    elif attack_name == 'rfgsm':
        return torchattacks.RFGSM(model, eps=attack_strength, alpha=attack_strength)
    elif attack_name == 'auto-attack':
        return torchattacks.AutoAttack(model, eps=attack_strength)
    elif attack_name == 'mifgsm':
        return torckattacks.MIFGSM(model, eps=attack_strength, steps=steps)
    elif attack_name == 'square':
        return torchattacks.Square(model, eps=attack_strength)
    elif attack_name == 'fab':
        return torchattacks.FAB(model, eps=attack_strength)
    elif attack_name == 'one-pixel':
        return torchattacks.OnePixel(model)
    elif attack_name == 'gn':
        return torchattacks.GN(model, sigma=attack_strength)
    elif attack_name == 'apgd':
        return torchattacks.APGD(model, eps=attack_strength)
    elif attack_name == 'eotpgd':
        return torchattacks.EOTPGD(model, eps=attack_strength, steps=steps, alpha=attack_strength/(steps*.5))
    elif attack_name == 'pgddlr':
        return torchattacks.PGDDLR(model, eps=attack_strength, steps=steps, alpha=attack_strength/(steps*.5))
    elif attack_name == 'ffgsm':
        return torchattacks.FFGSM(model, eps=attack_strength, alpha=attack_strength)
    elif attack_name == 'sparsefool':
        return torchattacks.SparseFool(model)

    else:
        print("Attack not valid")
        sys.exit(-1)

def get_defense():
  pass
