# library imports
import shutil
import os
# repo file imports
from settings import current_settings
import database

""" config files copied from drive """

if not current_settings.local:
    print("HERE\n\n\n\n\nHERE")
    os.mkdir('/root/.aws/')
    creds = '/content/drive/MyDrive/feature-attribution/config/'+current_settings.name+'-credentials'
    shutil.copy(creds, '/root/.aws/credentials')
    shutil.copy('/content/drive/MyDrive/feature-attribution/config/config','/root/.aws/')

""" global vars """
database = database.Database()
