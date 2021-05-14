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
                    accuracy='n/a', loss='n/a', f1='n/a', description='none'):

        global current_settings


        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        assert attack in ['none', 'fgsm']
        assert defense in ['none']
        assert dataset in ['cifar', 'mnist', 'imagenet']
        assert model in ['resnet', 'VGG16']

        self.table.put_item(
        Item={
            'id': current_settings.current_result_id,
            'attack': attack,
            'defense': defense,
            'attack_strength': str(attack_strength),
            'model': model,
            'dataset': dataset,
            'accuracy': str(accuracy),
            'loss': str(loss),
            'f1': str(f1),
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
        assert model in ['resnet', 'VGG16']

        response = table.get_item(
        Key={
            'username': 'janedoe',
            'last_name': 'Doe'
        })
        item = response['Item']
        print(item)
