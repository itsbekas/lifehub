import time

from sqlalchemy import create_engine

from lifehub.config.constants import DATABASE_URL


def check_mariadb(timeout=60, interval=5) -> None:
    start_time = time.time()
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            connection = engine.connect()
            connection.close()
            print("Successfully connected to MariaDB")
            break
        except Exception:
            if time.time() - start_time > timeout:
                print("Could not connect to MariaDB within the timeout period")
                exit(1)
            print("MariaDB not ready, waiting...")
            time.sleep(interval)


def pre_run_checks():
    check_mariadb()
