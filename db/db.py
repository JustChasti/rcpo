from time import sleep

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from loguru import logger

from db.config import base_name, base_host, base_user, base_password


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    games = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)


data = {
    'drivername': 'mysql',
    'host': base_host,
    'username': base_user,
    'password': base_password,
    'database': base_name
}


while True:
    try:
        # engine = create_engine(f"mysql://{base_user}:{base_password}@{base_host}/{base_name}")
        engine = create_engine(URL(**data))
        engine.connect()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)