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
#   - l2
#   - loss
#   - description: any interesting info to add

from settings import current_settings
import boto3
from boto3.dynamodb.conditions import Key
from result import Result

class Database:
    def __init__(self):
        """ dynamoDB setup """
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('results2')
        print(self.table.creation_date_time)

    def load_all(self):
        results = []
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']
        for i in items:
            results.append(Result('database', i))

        return results



    def write_result(self, attack='none', defense='none', attack_strength='n/a',
                    model=None, dataset=None,
                    accuracy='n/a', loss='n/a', l2='n/a', description='none'):

        global current_settings


        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        assert attack in ['none', 'fgsm']
        assert defense in ['none']
        assert dataset in ['cifar', 'mnist', 'imagenet']


        self.table.put_item(
        Item={
            'id': self.get_id(),
            'attack': attack,
            'defense': defense,
            'attack_strength': str(attack_strength),
            'model': model,
            'dataset': dataset,
            'accuracy': str(accuracy),
            'loss': str(loss),
            'l2': str(l2),
            'description': description,

        })

    def get_result(self, attack='non', defense='none', attack_strength='none',
                    model=None, dataset=None):

        global current_settings


        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        assert attack in ['none', 'fgsm']
        assert defense in ['none']
        assert dataset in ['cifar', 'mnist', 'imagenet']

        response = table.get_item(
        Key={
            'username': 'janedoe',
            'last_name': 'Doe'
        })
        item = response['Item']
        print(item)

    def delete(self, id):
        response = self.table.delete_item(
            Key={
                'id': id,
            })


    def get_id(self):
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']
        max_id = -1
        for i in items:
            if int(i['id']) > max_id:
                max_id = int(i['id'])

        return max_id+1

    def show_all(self):
        print('\n** All Results in Database **')
        print('-------------------------------------------------------------------------------')
        print('id  attack     defense    atck-stren  model         dataset   acc    loss   l2')
        print('-------------------------------------------------------------------------------')
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']
        if len(items) == 0:
            print("No items in database\n")
        for i in reversed(items):
            index = i['model'].find('-')
            name = i['model'][index+1:]
            print(f"{i['id']:2}  {i['attack']:10} {i['defense']:10} {i['attack_strength']:12}"
                f"{name:13} {i['dataset']:9} {i['accuracy']:6} {i['loss'][:5]:6} {i['l2']:5}")
        print()
