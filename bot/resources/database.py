from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.declarative as dec

DATABASE_FILE = 'resources/database.db'

SqlAlchemyBase = dec.declarative_base()

engine = create_engine(f'sqlite:///{DATABASE_FILE}')
factory = sessionmaker(bind=engine)
db_session = factory()
