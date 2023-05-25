# built-ins
import time
import random
from configparser import ConfigParser

# Single psycopg2 import whose
# purpose is to provide:
#
# a. Interface to build the cursor,
#    i.e. connection pool.
# b. The cursor will provide the resources
#    to execute or queries.
from psycopg2 import connect


# Again, this could be set before running the
# app in some other fashion
__ENV__ = "development"

# Again, initialize "dotenv" for secure practices
config = ConfigParser()
config.read("config.ini")


#
# 1. Define the connection layer
def connection():
    conn = connect(
        dbname=config.get(__ENV__, "database_name"),
        user=config.get(__ENV__, "database_user"),
        password=config.get(__ENV__, "database_password"),
        host=config.get(__ENV__, "database_host"),
        port=config.get(__ENV__, "database_port"),
    )
    # configure
    conn.autocommit = True
    return conn.cursor()


#
# 2. Define a mapper to parse raw tuple
#    data incoming from the query into a
#    reusable dictionary.
def map_users_tuple(user_tuple: tuple) -> dict:
    (
        uuid,
        username,
        email,
        password,
        verified,
        verified_at,
        access_policy,
        created_at,
        updated_at,
        deleted_at,
    ) = user_tuple

    return dict(
        uuid=uuid,
        username=username,
        email=email,
        password=password,
        verified=verified,
        verified_at=verified_at,
        access_policy=access_policy,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
    )


#
# 3. Define a DAO resource to perform
#    the insert transaction.
def create_user(conn, username: str, email: str, password: str) -> list:
    sql = """
    INSERT INTO users (
        username,
        email,
        password
    ) SELECT
        %(username)s,
        %(email)s,
    CRYPT(%(password)s, GEN_SALT('bf'))
    RETURNING *;
    """
    params = dict(
        username=username,
        email=email,
        password=password,
    )
    conn.execute(sql, params)

    result = conn.fetchall()
    result = list(map(map_users_tuple, result))
    return result
