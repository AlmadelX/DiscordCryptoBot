import sqlalchemy

from bot.services.db_session import SqlAlchemyBase


class Setting(SqlAlchemyBase):
    __tablename__ = 'settings'

    key = sqlalchemy.Column(
        sqlalchemy.Text, nullable=False, primary_key=True, unique=True)
    value = sqlalchemy.Column(sqlalchemy.Text)
