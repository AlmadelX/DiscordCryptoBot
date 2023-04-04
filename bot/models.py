import sqlalchemy

from bot.services.db_session import SqlAlchemyBase


class Setting(SqlAlchemyBase):
    __tablename__ = 'settings'

    key = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    value = sqlalchemy.Column(sqlalchemy.Text, nullable=False)


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, primary_key=True, unique=True)
    lang = sqlalchemy.Column(sqlalchemy.Text, nullable=False)


class Text(SqlAlchemyBase):
    __tablename__ = 'texts'

    name = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    eng = sqlalchemy.Column(sqlalchemy.Text)
    rus = sqlalchemy.Column(sqlalchemy.Text)


class Server(SqlAlchemyBase):
    __tablename__ = 'servers'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False, unique=True)


class Subscription(SqlAlchemyBase):
    __tablename__ = 'subscriptions'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        'users.id'), nullable=False, unique=True)
    server_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        'servers.id'), nullable=False, primary_key=True, unique=True)
