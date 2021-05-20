import colorama
from colorama import Fore, Back, Style
class Settings:
    def __init__(self):
        with open('config/config.txt', 'r') as f:
            config_dict = dict(line.strip().split(':') for line in f)
        self.name = config_dict['user']
        self.model_set = config_dict['model_set']
        if config_dict['local'] == 'False':
            self.local = False
        elif config_dict['local'] == 'True':
            self.local = True
        else:
            print('Error: wrong value for local in config')
            sys.exit(0)

        self.datasets = config_dict['datasets'].split(',')
        if self.local:
            self.file_name = './config/'+self.name+'-settings.txt'
        if not self.local:
            self.file_name = './config/'+self.name+'-settings.txt'#'/content/drive/MyDrive/feature-attribution/config/'+name+'-settings'
        settings = self.read_settings_file()


        self.model_name = settings['model_name']
        self.dataset = settings['dataset']


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
            'model_set': self.model_set
        }
        return settings

    def print_settings(self):
        print('\nSettings Initalized as')
        print('++++++++++++++++++++++++')
        print(f'{Back.MAGENTA}user:\t\t\t{self.name}')
        print(f'model_set:\t\t{self.model_set}')
        print(f'loaded datasets:\t{self.datasets}')
        print(f'model_name:\t\t{self.model_name}')
        print(f'dataset:\t\t{self.dataset}')
        print(Style.RESET_ALL)
        print()


    def set_model_name(name):
        self.model_name = name
        self.write_settings_file()

    def set_dataset(dataset):
        self.dataset = set_dataset
        self.write_settings_file()




current_settings = Settings()
