import os
from argparse import ArgumentParser
from configparser import ConfigParser
from datetime import datetime
from time import time

# SQLAlchemy imports
from sqlalchemy import create_engine, Column, DateTime, String, UUID, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Query
from sqlalchemy.sql import select, insert, text

# profiler
import memory_profiler
import profile


__ENV__ = "development"

# Initialize "argv"
cli = ArgumentParser()
cli.add_argument("--num-records", type=int, dest="num_records", default=100)
cli.add_argument("--verbose", action="store_true", dest="verbose")
args = cli.parse_args()

# Initialize "dotenv"
config = ConfigParser()
config.read("config.ini")

# ORM setup
Model = declarative_base(name="Model")


class User(Model):
    __tablename__ = "users"
    uuid = Column(
        "uuid",
        UUID,
        primary_key=True,
        default=None,  # horribly as uuid1()
        nullable=True,  # won't help at all
    )
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)


class Todo(Model):
    __tablename__ = "todos"
    uuid = Column(
        "uuid",
        UUID,
        primary_key=True,
        default=None,  # horribly as uuid1()
        nullable=True,  # won't help at all
    )
    name = Column(String(255), nullable=False)
    user_uuid = Column("user_uuid", UUID, ForeignKey(User.uuid), nullable=False)
    due_to = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)


def create_user(conn, username, password):
    query = (
        insert(User).values(username=username, password=password).returning(User.uuid)
    )

    result = conn.execute(query)
    conn.commit()
    return result.one()


def create_todo(conn, name, user_uuid, due_to):
    query = (
        insert(Todo)
        .values(name=name, user_uuid=user_uuid, due_to=due_to)
        .returning(Todo.uuid)
    )

    result = conn.execute(query)
    conn.commit()
    return result.one()


def connection():
    engine = create_engine(config.get(__ENV__, "database_uri"))
    sess = scoped_session(sessionmaker(bind=engine))
    return engine, sess


def init():
    engine, conn = connection()

    # Piece of code intentionally left to
    # highlight issues found at lines 33/49
    # regarding UUIDs managed by python.
    #
    # Apply "migrations"
    # Model.metadata.create_all(engine)

    return conn


@memory_profiler.profile
def main():
    conn = init()

    for i in range(args.num_records):
        user = create_user(conn, f"user-{i}", f"pass-{i}")
        todo = create_todo(conn, f"todo-{i}", str(user[0]), datetime.now())


if __name__ == "__main__":
    start = time()

    if args.verbose:
        profile.run("main()")
    else:
        main()

    end = time() - start
    print(f"elapsed time: {end}")
