from sqlalchemy import Column, Integer, String, DateTime, func, event, UniqueConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint('email', 'user_id', name='unique_email_user'),
    )
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    birthdate = Column(DateTime)
    days_of_year = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


@event.listens_for(Contact, 'before_insert')
def updated_birthdate(mapper, conn, target):
    """
    The updated_birthdate function is a SQLAlchemy event listener that will be called whenever the birthdate attribute of an instance of the Person class changes.
    
    :param mapper: Map the class attributes to database columns
    :param conn: Access the database connection
    :param target: Pass the instance of the model that is being updated
    :return: The number of days in the year for a given birthdate
    :doc-author: Trelent
    """
    if target.birthdate:
        dn = target.birthdate.replace(day=1, month=1)
        td = target.birthdate - dn
        target.days_of_year = td.days


@event.listens_for(Contact, 'before_update')
def updated_birthdate(mapper, conn, target):
    """
    The updated_birthdate function is a SQLAlchemy event listener that will be called
    whenever the birthdate attribute of an instance of the Person class is updated.  It
    will calculate how many days into the year that date falls and store it in a new
    attribute, days_of_year.
    
    :param mapper: Access the mapped class
    :param conn: Connect to the database
    :param target: Access the object being mapped
    :return: The number of days since the 1st of january
    :doc-author: Trelent
    """
    if target.birthdate:
        dn = target.birthdate.replace(day=1, month=1)
        td = target.birthdate - dn
        target.days_of_year = td.days


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

