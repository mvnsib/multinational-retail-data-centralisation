import pandas as pd
import numpy as np


class DataCleaning:
    def __init__(self):
        pass

    def clean_null(self, table):
        table = pd.DataFrame(table)
        table.replace("NULL", np.NaN, inplace=True)
        table.dropna(
            subset=["date_of_birth", "email_address", "user_uuid"],
            how="any",
            axis=0,
            inplace=True,
        )
        return table

    def clean_date(self, table, column):
        table[column] = pd.to_datetime(table[column], errors="coerce")
        return table[column]

    def clean_user_data(self, user_data):
        self.clean_date(user_data, "date_of_birth")
        self.clean_date(user_data, "join_date")
        self.clean_null(user_data)
        return user_data

    def clean_card_data(self, card_df):
        card_df["card_number"] = card_df["card_number"].apply(str)
        card_df.replace("NULL", np.NaN, inplace=True)
        card_df.dropna(subset=["card_number"], how="any", axis=0, inplace=True)

        return card_df

    def called_clean_store_data(self, store_df):
        store_df = store_df.reset_index(drop=True)
        store_df["staff_numbers"] = pd.to_numeric(
            store_df["staff_numbers"], errors="coerce"
        )
        store_df["opening_date"] = pd.to_datetime(
            store_df["opening_date"], errors="coerce"
        )
        store_df.replace("NULL", np.NaN, inplace=True)
        store_df = store_df.replace("NULL", pd.NA)
        store_df = store_df.drop(columns=["lat"])
        store_df.dropna(subset=["staff_numbers"], how="any", inplace=True)
        store_df.dropna(subset=["opening_date"], how="any", inplace=True)
        store_df.dropna(subset=["latitude"], how="any", inplace=True)

        return store_df

    def convert_product_weights(self, products_df):
        products_df["weight"] = products_df["weight"].str.lower()

        def convert_to_kg(weight_str):
            weight_str = str(weight_str)
            weight_str = weight_str.replace(" .", "")
            weight_str = weight_str.replace(" ", "")

            if weight_str.endswith("kg"):
                return weight_str
            elif weight_str.endswith("ml"):
                if "x" in weight_str:
                    weight_str = weight_str.replace("ml", "")
                    weight_str = weight_str.replace("x", "*")
                    weight_str = eval(weight_str)
                    weight_str = float(weight_str) / 1000
                    weight_str = f"{str(weight_str)}kg"

                else:
                    weight_str = weight_str.replace("ml", "")
                    weight_str = float(weight_str) / 1000
                    weight_str = f"{str(weight_str)}kg"
                    return weight_str
            elif weight_str.endswith("g"):
                if "x" in weight_str:
                    weight_str = weight_str.replace("g", "")
                    weight_str = weight_str.replace("x", "*")
                    weight_str = eval(weight_str)
                    weight_str = float(weight_str) / 1000
                    weight_str = f"{str(weight_str)}kg"
                else:
                    weight_str = weight_str.replace("g", "")
                    weight_str = float(weight_str) / 1000
                    weight_str = f"{str(weight_str)}kg"
                return weight_str
            return weight_str

        products_df["weight"] = products_df["weight"].apply(convert_to_kg)

        products_df = products_df.drop(columns=["Unnamed: 0"])

        return products_df

    def clean_products_data(self, products_df):
        products_df["date_added"] = pd.to_datetime(
            products_df["date_added"], errors="coerce"
        )
        products_df.dropna(subset=["date_added"], how="any", inplace=True)
        products_df.reset_index(inplace=True)
        return products_df

    def clean_orders_data(self, order_df):
        order_df.drop("level_0", axis=1, inplace=True)
        order_df = order_df.drop(columns=["first_name", "last_name", "1"])

        return order_df
