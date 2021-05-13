class Settings:
    def __init__(self):
        with open('config/config.txt', 'r') as f:
            config_dict = dict(line.strip().split(':') for line in f)
        self.name = config_dict['user']
        if config_dict['local'] == 'False':
            self.local = False
        else:
            self.local = True

        self.local = bool(config_dict['local'])
        self.datasets = config_dict['datasets'].split(',')
        if self.local:
            self.file_name = file_name = './config/'+self.name+'-settings.txt'
        if not self.local:
            self.file_name = '/content/drive/MyDrive/feature-attribution/config/'+name+'-settings'
        settings = self.read_settings_file()


        self.model_name = settings['model_name']
        self.dataset = settings['dataset']
        self.current_result_id = int(settings['current_result_id'])


    def read_settings_file(self):
        with open(self.file_name, 'r') as f:
            d = dict(line.strip().split(':') for line in f)
        return d

    def write_settings_file(self):
        with open(self.file_name, 'w') as f:
            for key, value in self.get_settings_dict().items():
                f.write('%s:%s\n' % (key, value))

    def get_settings_dict(self):
        settings = {
            'model_name': self.model_name,
            'dataset': self.dataset,
            'current_result_id': self.current_result_id
        }
        return settings

    def print_settings(self):
        print('\nSettings Initalized as')
        print('++++++++++++++++++++++++')
        print(f'user:\t\t{self.name}')
        print(f'model_name:\t{self.model_name}')
        print(f'dataset:\t{self.dataset}')
        print(f'current result id: {self.current_result_id}')
        print(f'loaded datasets: {self.datasets}')


    def set_model_name(name):
        self.model_name = name
        self.write_settings_file()

    def set_dataset(dataset):
        self.dataset = set_dataset
        self.write_settings_file()

    def set_current_results_id(id):
        self.current_result_id = id
        self.write_settings_file()



current_settings = Settings()
