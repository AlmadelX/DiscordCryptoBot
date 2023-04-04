from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative as dec

from bot.data.config import DATABASE_PATH

SqlAlchemyBase = dec.declarative_base()

engine = create_engine(f'sqlite:///{DATABASE_PATH}')
factory = sessionmaker(bind=engine)
db_session = factory()
