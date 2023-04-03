import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
settings = config['settings']

# Load constants
BOT_TOKEN = settings['bot_token'].strip().replace(' ', '')
LOGS_PATH = settings['logs_path'].strip().replace(' ', '')
