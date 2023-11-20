import pandas as pd
import requests
from sqlalchemy import text
import tabula
import json
import boto3


class DataExtractor:
    def __init__(self):
        self.x_api_key = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        self.num_stores_url = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        )
        self.store_data_url = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
        )

    def read_rds_table(self, database_connector, table):
        engine = database_connector.init_db_engine(
            database_connector.read_db_creds("db_creds.yaml")
        )
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            data = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(data, columns=columns)
            return df
            # return pd.read_sql_table(table, con=conn)

    def retrieve_pdf_data(self, link):
        df = pd.concat(tabula.read_pdf(link, pages="all"), ignore_index=True)
        return df

    def list_number_of_stores(self):
        api_url_base = self.num_stores_url
        key = self.x_api_key
        response = requests.get(api_url_base, headers=key).content
        result = json.loads(response)
        return result["number_stores"]

    def retrieve_stores_data(self):
        # pd dataframe save
        data = []
        number_stores = self.list_number_of_stores()
        key = self.x_api_key
        for store in range(number_stores):
            api_url_base = f"{self.store_data_url}{store}"
            api_url_base = str(api_url_base)
            response = requests.get(api_url_base, headers=key)
            # content = response.text
            # result = json.loads(content)
            data.append(pd.json_normalize(response.json()))

        # df = pd.DataFrame(data)

        return pd.concat(data)

    def extract_from_s3(self, bucket, key):
        s3_client = boto3.client("s3")

        response = s3_client.get_object(Bucket=bucket, Key=key)
        data = response["Body"]
        df = pd.read_csv(data)
        return df

    def extract_from_link(self, url):
        s3_client = boto3.resource("s3")
        url = url.replace("https://", "")
        bucket, key = url.split("/", 1)
        bucket = "data-handling-public"
        obj = s3_client.Object(bucket, key)
        body = obj.get()["Body"]
        df = pd.read_json(body)
        df = df.reset_index(drop=True)

        return df
