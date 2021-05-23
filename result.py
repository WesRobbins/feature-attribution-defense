class Result:
    def __init__(self, input_type, data):
        assert input_type in ['database', 'runtime']
        self.input_type = input_type
        if input_type == 'database':
            self.load_from_database(data)
        elif input_type == 'runtime':
            self.load_from_runtime(data)


    def load_from_database(self, data):
        self.id = int(data['id'])
        self.model = data['model']
        self.dataset = data['dataset']
        self.attack = data['attack']
        self.defense = data['defense']
        self.description = data['description']
        if data['attack_strength'] in ['none', 'n/a']: self.attack_strength = 'n/a'
        else: self.attack_strength = float(data['attack_strength'])
        if data['loss'] == 'n/a': self.loss = 'n/a'
        else: self.loss = float(data['loss'])
        if data['accuracy'] == 'n/a': self.accuracy = 'n/a'
        else: self.accuracy = float(data['accuracy'])
        if data['l2'] == 'n/a': self.l2 = 'n/a'
        else: self.l2 = float(data['accuracy'])

    def get_dict(self):
        x = {'id':self.id,
            'model':self.model,
            'dataset':self.dataset,
            'attack':self.attack,
            'defense':self.defense,
            'attack_strength':self.attack_strength,
            'loss':self.loss,
            'accuracy':self.accuracy,
            'l2': self.l2
            }
        return x




""" returns results that match parameters
    - params can be lists or single string
    - models are required               """
def get_results(results, id=None, models=None, attacks='none', defenses='none',
        dataset='cifar', attack_strengths=None):

    if type(attack_strengths) == float:
        attack_strengths = [attack_strengths]

    vals = []
    for i in results:
        if id:
            if int(i.id) not in id:
                continue
        if attack_strengths:
            if type(i.attack_strength) == str:
                continue
            elif i.attack_strength not in attack_strengths:
                continue
        if i.model not in models:
            continue
        if i.attack not in attacks:
            continue
        if i.defense not in defenses:
            continue
        if i.dataset not in dataset:
            continue
        vals.append(i)

    return vals

def axis_arrays(results, axis='attack_strength', metric='accuracy'):
    axises = ['model', 'attack', 'defense', 'dataset', 'attack_strength']
    assert axis in axises

    axises.remove(axis)
    vals = {}
    for i in results:
        i = i.get_dict()
        li = []
        for ax in axises:
            li.append(i[ax])
        li = tuple(li)
        if li not in vals.keys():
            vals[li] = []
        vals[li].append((i[axis], i[metric]))

    return vals
