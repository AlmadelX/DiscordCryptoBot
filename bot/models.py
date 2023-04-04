import sqlalchemy

from bot.services.db_session import SqlAlchemyBase


class Setting(SqlAlchemyBase):
    __tablename__ = 'settings'

    key = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    value = sqlalchemy.Column(sqlalchemy.Text, nullable=False)


class Language(SqlAlchemyBase):
    __tablename__ = 'languages'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, primary_key=True, unique=True)
    lang = sqlalchemy.Column(sqlalchemy.Text, nullable=False)


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    name = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    eng = sqlalchemy.Column(sqlalchemy.Text)
    rus = sqlalchemy.Column(sqlalchemy.Text)
