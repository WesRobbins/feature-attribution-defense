class Result:
    def __init__(self, input_type, data, model_set_names):
        assert input_type in ['database', 'runtime']
        self.input_type = input_type
        if input_type == 'database':
            self.load_from_database(data)
        elif input_type == 'runtime':
            self.load_from_runtime(data)

        self.model_set_names = model_set_names

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




    def get(id=None, model=None):
        pass
