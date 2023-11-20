import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import text


class DatabaseConnector:
    def __init__(self):
        pass

    def read_db_creds(self, filename):
        with open(filename, "r") as stream:
            try:
                creds = yaml.safe_load(stream)
                print(creds)
                return creds

            except yaml.YAMLError as exc:
                print(exc)

    def init_db_engine(self, creds):
        engine = create_engine(
            f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        )
        print("connection made")
        return engine

    def list_db_tables(self, engine):
        inspector = inspect(engine)
        return inspector.get_table_names()

    def upload_to_db(self, df, name, creds):
        engine = create_engine(
            f"{creds['LOCAL_DATABASE_TYPE']}+{creds['LOCAL_DB_API']}://{creds['LOCAL_USER']}:{creds['LOCAL_PASSWORD']}@{creds['LOCAL_HOST']}:{creds['LOCAL_PORT']}/{creds['LOCAL_DATABASE']}"
        )
        engine.connect()
        df.to_sql(name, engine, if_exists="replace")


if __name__ == "__main__":
    dbcon = DatabaseConnector()

    creds = dbcon.read_db_creds("db_creds.yaml")
    engine = dbcon.init_db_engine(creds)
    tables_list = dbcon.list_db_tables(engine)
    print(tables_list)

    with engine.begin() as conn:
        try:
            table = pd.read_sql_table(tables_list[1], con=conn)
            print(table)
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
