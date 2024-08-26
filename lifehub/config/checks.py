import sqlalchemy

from lifehub.config.constants import DATABASE_URL

def check_mariadb() -> None:
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
    except Exception as e:
        print("Could not connect to MariaDB")
        exit(1)

def pre_run_checks():
    check_mariadb()
    