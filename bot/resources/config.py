import configparser
from configparser import ConfigParser

from bot.resources.logging import logger

SETTINGS_FILE = 'resources/settings.ini'


class Config:

    @staticmethod
    def __get_setting(settings: dir, setting: str) -> str:
        return settings[setting].strip().replace(' ', '')

    @staticmethod
    def __get_admins(settings: dir) -> list[int]:
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

    def __init__(self):
        parser = ConfigParser()

        try:
            parser.read(SETTINGS_FILE)
            settings = parser['settings']

            self.bot_token = self.__get_setting(settings, 'bot_token')
            self.discord_token = self.__get_setting(settings, 'discord_token')
            self.bot_admins = self.__get_admins(settings)
        except EnvironmentError:
            logger.critical('Failed to load settings file')
            exit(-1)
        except configparser.Error:
            logger.critical('Failed to parse settings file')
            exit(-1)

        if len(self.bot_token) == 0:
            logger.critical('Telegram token is not specified')
            exit(-1)
        if len(self.discord_token) == 0:
            logger.critical('Discord token is not specified')
            exit(-1)
        if len(self.bot_admins) == 0:
            logger.error('Admins are not specified')


config = Config()
