### psycopg2 vs SQLAlchemy

This project is the begining of what could be a very exhausive research
_(and probably will be)_ about the differences between **SQL-native drivers** vs.
**ORM** libraries, and for the sake of simplicity and because it is one of my
favorite programming languages, I've chosen Python for coding the sample scripts.

> Disclaimer:
>
> The scripts provided may use simple read-write operations, therefore,
> if you're reading and you're a database enthusiast or even a DBA
> and would like to contribute with more scripts and/or additional approaches,
> feel free to raise a **Pull Request** or **Issue** with your ideas to enrich
> this project's scope.

Finally and worth to mention, in order to provide consistency across data,
I've decided to centralize migrations using `alembic`. This way, the comparisson
between technologies can be focused on common data structures.

---

### Scripts

- The `src/run_driver.py` script will initialize a single connection using then
  **psycopg2** PostgreSQL driver during the the program's lifecycle, and then it
  will iterate over the number of records provided via the `--num-records` argument
  _(by default 100)_.

  Once it finishes, it will provide the default profiling results via stdout.

  For verbose profiling report use the `--verbose` option.

- Differently from the `src/run_driver.py`, the `src/run_orm.py` will initialize
  the mapped tables into `Model` classes that will grant the necessary metadata
  to perform the write queries accordingly, therefore, the codebase is considerably
  verbose than the driver's approach.

### Set up

- Virtualenvironment

      python -m pip install virtualenv && \
      python -m virtualenv .env && \
      . .env/bin/activate && \
      python -m pip install -r requirements.txt

- Database

      sudo apt install docker-ce docker-compose && \
      docker-compose up

- Migration script

      ./build.sh

### Usage example

    ./build.sh && python src/run_driver.py --num-records 1000

    (.env) ubuntu@ubuntu:~/duel-psycopg2-vs-sqlalchemy$ ./build.sh && python src/run_driver.py --num-records 1000
     pg_terminate_backend
    ----------------------
    (0 rows)

    WARNING:  there is no transaction in progress
    COMMIT
    DROP DATABASE
    WARNING:  there is no transaction in progress
    COMMIT
    CREATE DATABASE
    WARNING:  there is no transaction in progress
    COMMIT
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> a3bb52d4a435, create extensions
    INFO  [alembic.runtime.migration] Running upgrade a3bb52d4a435 -> 04e722d53493, create_users
    INFO  [alembic.runtime.migration] Running upgrade 04e722d53493 -> d363a99a86a2, create_table_todos
      Filename: /home/erickv/Projects/playground_python/duel-psycopg2-vs-sqlalchemy/src/run_driver.py

    Line #    Mem usage    Increment  Occurrences   Line Contents
    =============================================================
      70     28.7 MiB     28.7 MiB           1   @memory_profiler.profile
      71                                         def main():
      72     28.7 MiB      0.0 MiB        1001       for i in range(args.num_records):
      73     28.7 MiB      0.0 MiB        1000           user = create_user(conn, f"user-{i}", f"pass-{i}")[0]
      74     28.7 MiB      0.0 MiB        1000           todo = create_todo(conn, user, f"todo-{i}", datetime.now())[0]


    elapsed time: 6.784499168395996

---

### Conclusions

> Codebase

- **Readability**

  It is evident that in the amount of code between these two scipts is not very
  diferent, but that's due to the nature of the implementation, which is really...
  **really** simple, and lacks of a business logic per se.

  However, we should consider that both programs were meant to highligh the simplest
  way to have a database interaction up and running without digressing too much in abstractions
  that may lead us to make complex and verbose database layers.

  - Connection

    It's clear that the driver-based syntax is simpler than the ORM's, since
    the initial connection setup it very intuitive... you connect and get the
    pool for later use.

    However, the ORM's set up process is quite extensive since it requires to
    initialize the engine driver and then open up a common session for further
    implementation, and not to mention that if you'd like to deletegate the
    table creation to it, you should bind the _Model_ metadata and the engine.

  - Queries

    I think that anyone could say that the SQL-native approach is complex
    since it requires using long SQL strings... **However!**, I think it isn't quite
    enough to discard the approach since the ORM's query syntax reembles SQL itself,
    so, in some sense, a developer should write _SQLish_ code anyways.

    In my opinion, one of the most frustrating aspects about using ORMs is that
    we up duplicating data structure, i.e., we have a table definition within our
    database and also within our program via _Models_, and sometimes, if we want
    full consistency between our application and the tables within the database,
    we shoud delegate the migrations to the ORM... this is mostly the case when
    designing applications that can change the database engine over time... which
    I think if it is a consideration to opt for using ORMs, then we're taking bad
    software design decisions.

> Experience

- Documentation

  In both cases, I had a great developement experience sice every release version
  is extensively documented, hence I had no issues setting up the necessary
  configurations to have my implementation satified.

  It is worth to mention that opting for an SQL-native approch may be difficult
  at the begining since it requires SQL knowledge ahead, however, getting to the
  basics of SQL, it becomes faster to implement simple and even more detailed
  query functions.

- Debugging

  Even if both approaches are very simple, I faced a major issues that may
  compromise implementation at long term.

  Initially is that since my entities were supporting **UUIDs as primary keys**
  instead of commnly used auto increment serial integers, it wasn't very _"organic"_
  to the ORM to handle such logic, hence, I had to default the `uuid` column to `None`,
  and delegate the logic to the database itself.

  That's because I noticed that if I had attempted
  to default UUID creation to Python _(ergo ORM)_, the timestamp fetched to generate
  the UUID v1 was getting freezed, i.e. wasn't changing over time, therefore I was
  facing a lot of UUID colission errors, and that was visible within the database,
  since every record was being registered under a common timestamp.

> Performance

- Time management

  At the begining, I noticed that the ORM program was resolving write operations
  faster than the SQL-based program, but that happened only for small ammounts of
  transactions.

  However, when increasing the amount of transactions, I began to notice that the
  ORM was falling behind a few seconds, which it isn't a big deal if I hand't took
  a look at the memory management of the ORM.

- Memory management

  For me, it was shoking that even if the time resolution wasn't a big deal for
  an ORM, the memory management was red flag.

  In summary, the ORM doubles the memory consumption per transaction and the
  amount of processes triggered under the hood is monstrous.

  I invite you to check out the scripts applyting the `--verbose` option to
  have a visualization of what I mean.

---

### Troubleshooting

In case you run with issues while setting up `psycopg2`,
run this command to make your machine compatible with
the driver.

      sudo apt install postgresql libpq-dev
