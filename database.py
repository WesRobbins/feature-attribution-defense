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
from utils import get_tuple, get_stren
import datetime
import decimal
from decimal import Decimal


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
        return items





    def write(self, model=None, dataset=None,
                    atk=None, defense=None, eps=None, atk_steps=None,
                    acc=None, loss=None, l2=None):

        # global current_settings
        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        item = self.make_item(model, dataset, atk, defense, eps, atk_steps, acc, loss, l2)

        self.table.put_item(Item=item)

    def get(self, id=None, attack='none', defense='none', attack_strength='none',
                    model=None, dataset='cifar'):

        global current_settings

        if model == None:
            model = current_settings.model_name
        if dataset == None:
            dataset = current_settings.dataset

        if id != None:
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

    def show_all(self):
        print('\n** All Results in Database **')
        print('---------------------------------------------------------------------------------------')
        print('id    attack     defense    atck-stren  model         dataset   acc    loss   l2')
        print('---------------------------------------------------------------------------------------')
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']

        items.sort(key=lambda x: (x['atk']))
        if len(items) == 0:
            print("No items in database\n")
        for i in reversed(items):
            if i['l2'] != 'n/a':
                l2 = "{:.2e}".format(float(i['l2']))
            else:
                l2 = i['l2']
            print(f"{i['id']:4}  {i['atk']:10} {i['defense']:10} {i['eps']:10}  "
                f"{i['model']:13} {i['dataset']:9} {i['acc']:6} {i['loss'][:5]:6} {l2}")
        print()

    def count(self):

        print('\n** All Results in Database **')
        print('---------------------------------------------------------------------------------------')
        print('attack     defense   coiunt  atck-stren  model         dataset   acc    loss   l2')
        print('---------------------------------------------------------------------------------------')
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']

        dict = {}

        if len(items) == 0:
            print("No items in database\n")
        for i in reversed(items):
            if i['attack'] in dict.keys():
                dict[i['attack']] += 1
            else:
                dict[i['attack']] = 1

            if len(i['attack_strength']) == 0:
                stren = 'n/a'
            else:
                stren = ''
                for j in i['attack_strength'].values():
                    stren += str(j)+','
                stren = stren[:-1]

        for i in dict:
            print(f"{i}     {dict[i]}")
        print()

    def find_missing(self, attack=None, defense='none', strens=True, steps=False, spec=True):
        response = self.table.scan(
            FilterExpression=Key('id').gte(0)
        )
        items = response['Items']
        possible = get_tuple(attack, defense, strens, steps)


        for i in items:
            if i['attack'] == attack and i['defense'] == defense:
                if 'eps' and 'steps' in i['attack_strength'].keys():
                    t = (i['model'], i['attack_strength']['eps'], int(i['attack_strength']['steps']))
                elif 'eps' in i['attack_strength'].keys():
                    t = (i['model'], i['attack_strength']['eps'])
                elif 'steps' in i['attack_strength'].keys():
                    t = (i['model'], int(i['attack_strength']['steps']))


                try:
                    possible.remove(t)
                except:
                    print(f'not found: {t}')

        print(possible)
        print(len(possible))

    def make_item(self, model=None, dataset=None,
                    atk=None, defense=None, eps=None, atk_steps=None,
                     acc=None, loss=None, l2=None):
        item = {}
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        item['id']=self.get_id()
        item['time'] = time
        if not model:
            item['model']='n/a'
        else:
            item['model'] = model
        if not dataset:
            item['dataset']='n/a'
        else:
            item['dataset']=dataset
        if not atk:
            item['atk']='n/a'
        else:
            item['atk']=atk
        if not eps:
            item['eps']='n/a'
        else:
            item['eps']=Decimal(str(eps))
        if not atk_steps:
            item['atk_steps']='n/a'
        else:
            item['atk_steps']=atk_steps
        if not defense:
            item['defense']='n/a'
        else:
            item['defense']=defense
        if not acc:
            item['acc']='n/a'
        else:
            item['acc']=Decimal(str(acc))
        if not loss:
            item['loss']='n/a'
        else:
            item['loss']=Decimal(str(loss))
        if not l2:
            item['l2']='n/a'
        else:
            item['l2']=Decimal(str(l2))

        return item
