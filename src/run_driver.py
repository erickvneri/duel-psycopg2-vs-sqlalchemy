import os
import psycopg2
import logging
from time import time
from datetime import datetime
from configparser import ConfigParser
from argparse import ArgumentParser

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


def connection():
    conn = psycopg2.connect(
        dbname=config.get(__ENV__, "database_name"),
        user=config.get(__ENV__, "database_user"),
        password=config.get(__ENV__, "database_password"),
        host=config.get(__ENV__, "database_host"),
        port=config.get(__ENV__, "database_port"),
    )
    # configure
    conn.autocommit = True
    return conn.cursor()


def create_user(conn, username, password):
    sql = """
    INSERT INTO users (username, password)
    VALUES (
        %(username)s,
        CRYPT(%(password)s, GEN_SALT('bf'))
    ) RETURNING uuid;
    """
    params = dict(username=username, password=password)
    conn.execute(sql, params)
    return conn.fetchone()


def create_todo(conn, user_uuid, name, due_to):
    sql = """
    INSERT INTO todos (user_uuid, name, due_to)
    VALUES (
        %(user_uuid)s,
        %(name)s,
        %(due_to)s
    ) RETURNING uuid;
    """
    params = dict(user_uuid=user_uuid, name=name, due_to=due_to)
    conn.execute(sql, params)
    return conn.fetchone()


conn = connection()


@memory_profiler.profile
def main():
    for i in range(args.num_records):
        user = create_user(conn, f"user-{i}", f"pass-{i}")[0]
        todo = create_todo(conn, user, f"todo-{i}", datetime.now())[0]


if __name__ == "__main__":
    start = time()

    if args.verbose:
        profile.run("main()")
    else:
        main()

    end = time() - start
    print(f"elapsed time: {end}")
