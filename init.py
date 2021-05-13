# python script for initializing notebook
#   - set up config files
#   - imports
#   - pip installs
#   - option to automatically load models into runtime

""" installs """
pip install boto3

""" config files copied from drive """
import shutil
shutil.copy('/content/drive/MyDrive/feature-attribution/config/credentials','/root/.aws/')
shutil.copy('/content/drive/MyDrive/feature-attribution/config/config','/root/.aws/')

""" global vars """
current_settings = Settings()

""" imports """
import boto3


class Settings:
    def __init__(self, name='wes'):
        self.file_name = file_name = '/content/drive/MyDrive/feature-attribution/config/'+name+'-settings'
        self.settings = read_settings_file(name)
        self.model_name = settings['model_name']
        self.dataset = settings['dataset']
        self.current_result_id = int(settings[''])


    def read_settings_file(self):
        with open(self.file_name, 'r') as f:
            d = dict(line.strip().split(':') for line in f)
        return d

    def write_settings_file(self):
        with open("myfile.txt", 'w') as f:
            for key, value in details.items():
                f.write('%s:%s\n' % (key, value))

    def get_settings_dict(self):
        settings = {
            'model_name': self.model_name,
            'dataset': self.dataset,
            'current_result_id': self.current_result_id
        }
        return settings
