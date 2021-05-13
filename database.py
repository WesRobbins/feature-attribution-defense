# read and write from AWS database

# result params:
#   - name:
#   - attack: name of attack
#       options: fgsm, todo...
#   - defense: name of defense
#       options:
#   - attack_strength : attack strength
#   - model: name of model
#       options:
#   - dataset: name of dataset
#       options: cifar, mnist, imagenet
#   - accuracy
#   - f1
#   - loss
#   - description: any interesting info to add


def write_result(attack='none', defense='none', attack_strength='none',
                model=current_settings.model_name, dataset=current_settings.dataset,
                accuracy='n/a', loss='n/a', f1='n/a', description='n/a'){
    assert attack in ['none', 'fgsm']
    assert defense in ['none']
    assert dataset in ['cifar', 'mnist', 'imagenet']
    assert model in ['resnet']

    table.put_item(
    Item={
        'id': current_settings.current_result_id,
        'attack': attack,
        'defense': defense,
        'attack_strength': str(attack_strength),
        'model': model,
        'dataset': 'dataset,
        'accuracy': str(accuracy),
        'loss': str(loss),
        'f1': str(f1),
        'description': description,
         
    })
