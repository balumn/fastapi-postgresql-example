from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    # Add the back-reference to the Profile model
    profile = relationship("Profile", uselist=False, back_populates="user", lazy="select")


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    user = relationship("Users", back_populates="profile", lazy="select")
    profile_picture = Column(String, nullable=True)


def model_to_dict(model):
    """
    A generic function that would convert all the basic fields of any models to json.

    :param model:
    :return:
    """
    if not model:
        return None

    # Get the list of columns in the model
    columns = model.__table__.columns.keys()

    # Create a dictionary containing the model's attributes and values using dot notation
    model_dict = {column: getattr(model, column) for column in columns}

    return model_dict
