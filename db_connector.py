import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import date, datetime, timedelta
import atexit
import warnings

warnings.filterwarnings("ignore")

load_dotenv()
db_pass = os.environ["DB_PASS"]

today = datetime.now().date()
week_ago = datetime.now().date() + timedelta(days=-14)

add_deal = (
    "INSERT INTO registry "
    "(deal, prices, supplier, product, date) "
    "VALUES (%s, %s, %s, %s, %s)"
)
get_deal = (
    "SELECT id, deal, prices, supplier, product, date FROM registry "
    f"WHERE date BETWEEN '{week_ago}' AND '{today}'"
)
get_all_deal = "SELECT id, deal, prices, supplier, product, date, price_check, currency_check FROM registry"

cnx = mysql.connector.connect(
    user="admin",
    password=db_pass,
    host="127.0.0.1",
    database="deals",
    use_pure=True,
    port="3306",
)

cursor = cnx.cursor()


def insert_deals(df):
    for index, row in df.iterrows():
        data_deal = (
            row["deal"],
            row["prices"],
            row["supplier"],
            row["product"],
            today,
        )
        cursor.execute(add_deal, data_deal)
        emp_no = cursor.lastrowid
        print(emp_no)
    cnx.commit()


def get_deals():
    data = pd.read_sql(get_deal, cnx)
    print(data)
    return data


def get_all_deals():
    data = pd.read_sql(get_all_deal, cnx)
    print(data)
    return data


def update_deals(df):  # TODO
    update_deal = (
        "UPDATE registry " "SET price_check = %s, currency_check= %s " "WHERE id = %s"
    )
    for index, row in df.iterrows():
        data_deal = (row["price_check"], row["currency_check"], row["id"])
        cursor.execute(update_deal, data_deal)
    cnx.commit()


def close_cn():
    cursor.close()
    cnx.close()
    print("DB connection has just been closed.")


atexit.register(close_cn)
