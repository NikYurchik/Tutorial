from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings


username = settings.postgres_user
password = settings.postgres_password
domain = settings.postgres_db
port = settings.postgres_port
database = settings.postgres_db
URL = settings.sqlalchemy_database_url

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
