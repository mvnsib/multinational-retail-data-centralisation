import pandas as pd
import numpy as np
import re


class DataCleaning:
    def __init__(self):
        pass

    # def clean_null(self, table):
    #     table = pd.DataFrame(table)
    #     table.replace("NULL", np.NaN, inplace=True)
    #     table.dropna(
    #         subset=["date_of_birth", "email_address", "user_uuid"],
    #         how="any",
    #         axis=0,
    #         inplace=True,
    #     )
    #     return table

    # def clean_date(self, table, column):
    #     table[column] = pd.to_datetime(table[column], errors="coerce")
    #     return table[column]

    def clean_user_data(self, user_df):
        user_df["date_of_birth"] = pd.to_datetime(
            user_df["date_of_birth"], errors="coerce"
        )
        user_df["join_date"] = pd.to_datetime(user_df["join_date"], errors="coerce")
        print(user_df.head())
        user_df.replace("NULL", np.NaN, inplace=True)
        user_df.dropna(
            subset=["date_of_birth", "email_address", "user_uuid"],
            how="any",
            inplace=True,
        )

        return user_df

    def clean_card_data(self, card_df):
        card_df["card_number"] = card_df["card_number"].apply(str)
        card_df["card_number"] = card_df["card_number"].str.replace("?", "")
        card_df.replace("NULL", np.NaN, inplace=True)
        card_df["date_payment_confirmed"] = pd.to_datetime(
            card_df["date_payment_confirmed"], errors="coerce"
        )
        card_df.dropna(
            subset=["date_payment_confirmed"], how="any", axis=0, inplace=True
        )

        return card_df

    def called_clean_store_data(self, store_df):
        store_df = store_df.reset_index(drop=True)
        store_df.drop(columns=["lat"], inplace=True)
        store_df.replace("NULL", np.NaN, inplace=True)
        store_df["opening_date"] = pd.to_datetime(
            store_df["opening_date"], errors="coerce"
        )
        store_df.loc[[31, 179, 248, 341, 375], "staff_numbers"] = [78, 30, 80, 97, 39]
        # store_df["staff_numbers"] = store_df["staff_numbers"].astype(str)
        # store_df["staff_numbers"] = pd.to_numeric(
        #     store_df["staff_numbers"].apply(self.remove_letters),
        #     errors="coerce",
        #     downcast="integer",
        # )

        # store_df["staff_numbers"] = store_df["staff_numbers"].astype(int)
        # store_df.dropna(
        #     subset=["staff_numbers", "opening_date"], how="any", inplace=True
        # )
        store_df["staff_numbers"] = pd.to_numeric(
            store_df["staff_numbers"], errors="coerce"
        )
        store_df.dropna(subset=["staff_numbers"], axis=0, inplace=True)
        return store_df

    def clean_products_data(self, products_df):
        def clean_price(price_df):
            price_df = str(price_df)
            if "£" in price_df:
                price_df = price_df.replace("£", "")
            return price_df

        products_df.replace("NULL", np.NaN, inplace=True)
        products_df["date_added"] = pd.to_datetime(
            products_df["date_added"], errors="coerce"
        )
        # products_df.dropna(subset=["date_added"], how="any", axis=0, inplace=True)

        products_df["product_price"] = products_df["product_price"].apply(clean_price)
        products_df["product_price"] = pd.to_numeric(
            products_df["product_price"], errors="coerce"
        )
        products_df.dropna(subset=["product_price"], how="any", axis=0, inplace=True)
        products_df.to_csv("dim_products_unclean.csv", encoding="utf-8")
        return products_df

    def convert_product_weights(self, products_df):
        products_df["weight"] = products_df["weight"].str.lower()

        def convert_to_kg(weight_str):
            weight_str = str(weight_str)
            weight_str = weight_str.replace(" .", "")
            weight_str = weight_str.replace(" ", "")

            if weight_str.endswith("kg"):
                weight_str = weight_str.replace("kg", "")
                return weight_str
            elif weight_str.endswith("ml"):
                if "x" in weight_str:
                    weight_str = weight_str.replace("ml", "")
                    weight_str = weight_str.replace("x", "*")
                    weight_str = eval(weight_str)
                    weight_str = float(weight_str) / 1000
                    return weight_str
                else:
                    weight_str = weight_str.replace("ml", "")
                    weight_str = float(weight_str) / 1000

                    return weight_str
            elif weight_str.endswith("g"):
                if "x" in weight_str:
                    weight_str = weight_str.replace("g", "")
                    weight_str = weight_str.replace("x", "*")
                    weight_str = eval(weight_str)
                    weight_str = float(weight_str) / 1000
                    return weight_str

                else:
                    weight_str = weight_str.replace("g", "")
                    weight_str = float(weight_str) / 1000

                    return weight_str
            elif weight_str.endswith("oz"):
                weight_str = weight_str.replace("oz", "")
                weight_str = float(weight_str) * 0.0283495

            return weight_str

        products_df["weight"] = products_df["weight"].apply(convert_to_kg)

        products_df = products_df.drop(columns=["Unnamed: 0"])

        return products_df

    def clean_orders_data(self, order_df):
        order_df.drop("level_0", axis=1, inplace=True)
        order_df.drop(columns=["first_name", "last_name", "1"], axis=1, inplace=True)

        return order_df

    def clean_date_time(self, date_df):
        date_df["year"] = pd.to_numeric(date_df["year"], errors="coerce")
        date_df.dropna(subset=["year"], how="any", axis=0, inplace=True)
        return date_df
