from bot.utils.bot_logging import bot_logger

if __name__ == '__main__':
    bot_logger.debug('Debug')
    bot_logger.info('Info')
    bot_logger.warning('Warning')
    bot_logger.error('Error')
    bot_logger.critical('Critical')
