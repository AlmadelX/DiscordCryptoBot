import logging
import colorlog

LOGS_FILE = 'resources/logs.log'

# Console logger
console_formatter = colorlog.ColoredFormatter(
    '%(white)s[%(blue)s%(asctime)s%(white)s](%(purple)s%(filename)s:%(lineno)d%(white)s) %(green)s%(name)s %('
    'yellow)s%(levelname)s%(white)s: %(red)s%(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
console_handler.setLevel('WARNING')

# File logger
file_formatter = logging.Formatter(
    '[%(asctime)s](%(filename)s:%(lineno)d) %(name)s %(levelname)s: %(message)s'
)

file_handler = logging.FileHandler(LOGS_FILE, 'w', 'utf-8')
file_handler.setFormatter(file_formatter)
file_handler.setLevel('INFO')

# Setup logger
logging.basicConfig(
    level='NOTSET',
    handlers=[
        console_handler,
        file_handler
    ]
)

logger = logging.getLogger('bot')
