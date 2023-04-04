import sqlalchemy

from bot.services.db_session import SqlAlchemyBase


class Setting(SqlAlchemyBase):
    __tablename__ = 'settings'

    param = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    eng = sqlalchemy.Column(sqlalchemy.Text)
    rus = sqlalchemy.Column(sqlalchemy.Text)
