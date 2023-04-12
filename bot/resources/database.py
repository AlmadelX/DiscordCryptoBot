from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative as dec
from bot.resources.logging import logger

DATABASE_FILE = 'resources/database.db'

SqlAlchemyBase = dec.declarative_base()

try:
    engine = create_engine(f'sqlite:///{DATABASE_FILE}')
    factory = sessionmaker(bind=engine)
    db_session = factory()
except Exception:
    logger.critical('Database not found')
    exit(-1)
