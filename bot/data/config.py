import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
settings = config['settings']

LOGS_PATH = settings['logs_path'].strip().replace(' ', '')
