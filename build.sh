export PGPASSWORD='super_test_password'

##
# DB Connect callbacks
do_connect () {
  psql \
  -U postgres \
  --host 0.0.0.0 \
  --dbname postgres
}

##
# Terminate every transaction
# to proceed consistently.
do_connect \
<<SQL
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname='sample_database';
COMMIT;
SQL

##
# Drop databases
do_connect \
<<SQL
DROP DATABASE IF EXISTS sample_database;
COMMIT;
SQL

##
# Recreate databases
do_connect \
<<SQL
CREATE DATABASE sample_database;
COMMIT;
SQL

##
# Execute alembic migrations
export ENV='development'
alembic upgrade head
