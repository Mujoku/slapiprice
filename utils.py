from turtle import st
from typing import Callable
from ftfy import fix_text
import re
import numpy as np
import pandas as pd
from natura import Finder
from db_connector import get_all_deals, update_deals


def string_standardize(string: str) -> str:
    """This function takes a string and applies a number of methods to it so that the string is standarized for NLP.

    Args:
        string (str): _description_

    Returns:
        str: _description_
    """

    def rep_str(rep_pairs: dict, string: str, opr: Callable) -> str:
        for key, value in rep_pairs.items():
            if opr == "rep":
                string = string.replace(key, value)
            elif opr == "sub":
                string = re.sub(key, value, string)
            else:
                print("You didn't choose any string/regex method to be applied!")
        return string

    STDR: dict = {
        "—": "-",
        "–": "-",
        "―": "-",
        "…": "...",
        "´": "'",
        "&": "and",
        "-": " ",
        "–": " ",
    }
    STDS: dict = {
        r"(-|–)?\s\d*$": " ",
        r"""(-+|~+|!+|"+|;+|\?+|\++|\)+|\(+|\\+|\/+|\*+|\[+|\]+|}+|{+|\|+|_+)""": r" \1 ",
        r"\s*\n\s*": " \n ",
        r"(-|–)\s\d+$": " \n ",
        r"[^\S\n]+": " ",
    }

    string = rep_str(STDR, string, "rep")
    string = rep_str(STDS, string, "sub")
    string = fix_text(string)
    rx = re.findall(r"([LXIVCDM]+\b)", string)
    # string = string.encode("ascii", errors="ignore").decode()
    string = string.lower()
    string = string.title()
    for x in rx:
        string = string.replace(x.title(), x.upper())
    string = re.sub(r"(?<=\d)\s(?=\d)", " @ ", string)
    return string.strip()


def ngram(string, n=3):
    string = string.encode("ascii", errors="ignore").decode()
    string = string.lower()
    string = string.replace("&", "and")
    string = string.title()
    return string


def get_price(string):
    mf = Finder(converter=None, base_currency="EUR")
    res = mf.findall(string)
    return res


string = "The Sims 3 - Outdoor Living Stuff @ 1,99 eur - 200"

DB = get_all_deals()


def price_check(df):
    for index, row in DB.iterrows():
        mf = Finder(converter=None, base_currency="EUR")
        money = get_price(string_standardize(row["deal"]))
        price = [str(v.value) for v in money]
        currency = [v.currency for v in money]
        v = ", ".join(price)
        c = ", ".join(currency)
        print(row, price)
        DB.loc[index, "price_check"] = v
        DB.loc[index, "currency_check"] = c


price_check(DB)
update_deals(DB)
