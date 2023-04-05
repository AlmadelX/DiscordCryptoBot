import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

# Load settings
settings = config['settings']

BOT_TOKEN = settings['bot_token'].strip().replace(' ', '')
DISCORD_TOKEN = settings['discord_token'].strip().replace(' ', '')

# Constants
DATABASE_PATH = 'bot/data/database.db'
LOGS_PATH = 'bot/data/logs.log'


def get_admins() -> list[int]:
    admins = settings['bot_admins'].strip().replace(' ', '')

    if ',' in admins:
        admins = admins.split(',')
    else:
        if len(admins):
            admins = [admins]
        else:
            admins = []

    while '\r' in admins:
        admins.remove('\r')
    while '\n' in admins:
        admins.remove('\n')

    admins = list(map(int, admins))

    return admins
