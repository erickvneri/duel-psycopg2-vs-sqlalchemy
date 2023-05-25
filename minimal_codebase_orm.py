# built-ins
from configparser import ConfigParser
from hashlib import md5
from datetime import datetime
from uuid import uuid1

# SQLAlchemy imports whose
# general purpose are:
#
# a. To configure the connection.
# b. To initialize the entity abstractions.
# c. To build the queries.
#
# note: 'create_engine' is for connection,
# but belongs to root path of module's import, so...
#
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Query
from sqlalchemy import create_engine, Column, DateTime, String, UUID, Boolean, ARRAY
from sqlalchemy.sql import select, insert


# This could be set before running app in some other fashion
__ENV__ = "development"

# Initialize "dotenv" for secure practices
config = ConfigParser()
config.read("config.ini")


#
# 1. Define the connection layer
def connection():
    engine = create_engine(config.get(__ENV__, "database_uri"))
    sess = scoped_session(sessionmaker(bind=engine))
    return engine, sess


#
# 2. Initialize the model for further
# entity abstraction configuration.
Model = declarative_base(name=__name__)


#
# 3. Define the actual entity abstraction
class User(Model):
    __tablename__ = "users"

    uuid = Column(
        "uuid",
        UUID,
        primary_key=True,
        default=uuid1,
    )
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    access_policy = Column(ARRAY(String), default=["users", "profiles"])
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime)


#
# 4. Define a DAO resource to
# perform the insert transaction.
def create_user(conn, username: str, email: str, password: str) -> tuple:
    query = (
        insert(User)
        .values(username=username, email=email, password=password)
        .returning(User)
    )

    try:
        result = conn.execute(query)
        conn.commit()
        return result.one()
    except:
        pass
