import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# URI:  postgresql://username:password@domain:port/database
file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('REST_DB', 'USER')
password = config.get('REST_DB', 'PASSWORD')
domain = config.get('REST_DB', 'DOMAIN')
port = config.get('REST_DB', 'PORT')
database = config.get('REST_DB', 'DB_NAME')

URL = f"postgresql://{username}:{password}@{domain}:{port}/{database}"

engine = create_engine(URL, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
