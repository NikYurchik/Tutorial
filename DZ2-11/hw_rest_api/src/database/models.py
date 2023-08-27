from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, event
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthdate = Column(DateTime)
    days_of_year = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


@event.listens_for(Contact, 'before_insert')
def updated_birthdate(mapper, conn, target):
    if target.birthdate:
        dn = target.birthdate.replace(day=1, month=1)
        td = target.birthdate - dn
        target.days_of_year = td.days


@event.listens_for(Contact, 'before_update')
def updated_birthdate(mapper, conn, target):
    if target.birthdate:
        dn = target.birthdate.replace(day=1, month=1)
        td = target.birthdate - dn
        target.days_of_year = td.days
