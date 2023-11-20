import pandas as pd
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning


extractor = DataExtractor()
connector = DatabaseConnector()
cleaner = DataCleaning()


def upload_user():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()
    tables_list = connector.list_db_tables(engine)

    df_name = tables_list[1]
    df = cleaner.clean_user_data(extractor.read_rds_table(connector, df_name))
    print(df.head())

    cred = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(cred)
    engine.connect()
    connector.upload_to_db(df, "dim_users", creds)


def upload_dim_card_details():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()

    df = extractor.retrieve_pdf_data(
        "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    )
    print(df.head())
    print(df.info())

    df = cleaner.clean_card_data(df)
    connector.upload_to_db(df, "dim_card_details", creds)


def upload_store_data():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()
    # num_stores = extractor.list_number_of_stores()
    df = extractor.retrieve_stores_data()
    df = cleaner.called_clean_store_data(df)
    df.to_csv("dim_store_data.csv", encoding="utf-8")
    connector.upload_to_db(df, "dim_store_data", creds)


def upload_dim_products():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()
    # s3_url = "s3://data-handling-public/products.csv"
    bucket = "data-handling-public"
    key = "products.csv"
    df = extractor.extract_from_s3(bucket, key)
    print(df)
    df = cleaner.clean_products_data(df)
    df = cleaner.convert_product_weights(df)

    df.to_csv("dim_products.csv", encoding="utf-8")
    connector.upload_to_db(df, "dim_products", creds)


def upload_order_table():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()
    tables_list = connector.list_db_tables(engine)

    df_name = tables_list[2]
    order_df = pd.DataFrame(extractor.read_rds_table(connector, df_name))
    df = cleaner.clean_orders_data(order_df)
    connector.upload_to_db(df, "orders_table", creds)


def upload_dim_date_times():
    creds = connector.read_db_creds("db_creds.yaml")
    engine = connector.init_db_engine(creds)
    engine.connect()

    df = extractor.extract_from_link(
        "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
    )
    connector.upload_to_db(df, "dim_date_times", creds)


if __name__ == "__main__":
    # creds = connector.read_db_creds("db_creds.yaml")
    # engine = connector.init_db_engine(creds)
    # engine.connect()
    # upload_user()
    # upload_dim_card_details()
    # store_data()
    # upload_dim_products()
    # upload_order_table()
    upload_dim_date_times()
