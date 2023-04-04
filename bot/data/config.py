import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
settings = config['settings']

# Load constants
BOT_TOKEN = settings['bot_token'].strip().replace(' ', '')
DATABASE_PATH = settings['database_path'].strip().replace(' ', '')
LOGS_PATH = settings['logs_path'].strip().replace(' ', '')

def get_admins() -> list[int]:
    admins = settings['bot_admins'].strip().replace(' ', '')

    if ',' in admins:
        admins = admins.split(',')
    else:
        if len(admins):
            admins = [admins]
        else:
            admins = []
    
    while '\r' in admins: admins.remove('\r')
    while '\n' in admins: admins.remove('\n')

    admins = list(map(int, admins))

    return admins

