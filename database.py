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



    def write(self, attack='none', defense='none', attack_strength='n/a',
                    model=None, dataset=None,
                    accuracy='n/a', loss='n/a', l2='n/a', description='none'):

        global current_settings


        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        if type(attack_strength) == float:
            attack_strength = str(attack_strength)


        self.table.put_item(
        Item={
            'id': self.get_id(),
            'attack': attack,
            'defense': defense,
            'attack_strength': attack_strength,
            'model': model,
            'dataset': dataset,
            'accuracy': str(accuracy),
            'loss': str(loss),
            'l2': str(l2),
            'description': description,

        })

    def get(self, id=None, attack='none', defense='none', attack_strength='none',
                    model=None, dataset='cifar'):

        global current_settings

        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        if id:
            response = self.table.get_item(
            Key={'id': id})

        else:

            response = self.table.get_item(
            Key={
                'username': 'janedoe',
                'last_name': 'Doe'
            })
        item = response['Item']
        return item

    def delete(self, id, id2=None):
        if type(id) == list:
            for i in id:
                response = self.table.delete_item(
                    Key={
                        'id': i,
                    })
        elif not id2:
            response = self.table.delete_item(
                Key={
                    'id': id,
                })
        elif type(id) == int and id2:
            for i in range(id, id2+1):
                try:
                    response = self.table.delete_item(
                        Key={
                            'id': i,
                        })
                except:
                    printf(f'DB: no key {i}')

    def update(self, id, id2=None, dict=None):
        expr = 'set '
        count = 1
        for i in dict.keys():
            expr += i + '=:' + str(count) + ', '
            count += 1
        expr = expr[:-2]
        print(expr)

        count = 1
        attr = {}
        for i in dict.values():
            key = ':'+str(count)
            attr[key] = i
            count += 1

        print(attr)
        print()
        print()

        if type(id) == list:
            for i in id:
                response = self.table.update_item(
                    Key={'id': id},
                    # UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a",
                    ExpressionAttributeValues={
                        'model': 'Wes 2',
                    },
                    ReturnValues="UPDATED_NEW"
                )
                return response
        elif not id2:
            response = self.table.update_item(
                Key={'id': id},
                UpdateExpression=expr,
                ExpressionAttributeValues=attr,
                ReturnValues="UPDATED_NEW"
            )
            return response
        elif type(id) == int and id2:
            for i in range(id, id2+1):
                try:
                    response = self.table.delete_item(
                        Key={
                            'id': i,
                        })
                except:
                    printf(f'DB: no key {i}')



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

    def show_all(self, sort='id'):
        print('\n** All Results in Database **')
        print('---------------------------------------------------------------------------------------')
        print('id    attack     defense    atck-stren  model         dataset   acc    loss   l2')
        print('---------------------------------------------------------------------------------------')
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']
        items.sort(key=lambda x: x[sort])
        if len(items) == 0:
            print("No items in database\n")
        for i in reversed(items):
            if i['l2'] != 'n/a':
                l2 = "{:.2e}".format(float(i['l2']))
            else:
                l2 = i['l2']
            if len(i['attack_strength']) == 0:
                stren = 'n/a'
            else:
                stren = ''
                for j in i['attack_strength'].values():
                    stren += str(j)+','
                stren = stren[:-1]
            print(f"{i['id']:4}  {i['attack']:10} {i['defense']:10} {stren:12}"
                f"{i['model']:13} {i['dataset']:9} {i['accuracy']:6} {i['loss'][:5]:6} {l2}")
        print()
