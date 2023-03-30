### psycopg2 vs SQLAlchemy

This project is the begining of what could be a very exhausive research
_(and probably will be)_ about the differences between **SQL-native drivers** vs.
**ORM** libraries, and for the sake of simplicity and because it is one of my
favorite programming languages, I've chosen Python for coding the sample scripts.

Therefore, if you're reading this and would like to contribute with more scripts
and/or additional approaches, feel free to raise a PR with your ideas.

Also, in order to provide consistency across data, I've decided to centralize
migrations using `alembic`.

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
  verbose than the driver approach.

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

### Recommended usage

    ./build.sh && python src/run_driver.py --verbose --num-records 1000

---

### Troubleshooting

In case you run with issues while setting up `psycopg2`,
run this command to make your machine compatible with
the driver.

      sudo apt install postgresql libpq-dev
