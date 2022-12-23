from add_info import ai
import re
from xml.sax.saxutils import unescape


def prd(data):
    df = ai(data)
    for index, row in df.iterrows():
        product = unescape(re.sub("\s+|  \t+", " ", row["deal"]).strip())
        print(row["prices"])
        price = re.sub(r"((\s.*)|(.00))", "", row["prices"])
        unify_price = re.sub(r"[,]", ".", product)
        no_quantity = re.sub(r"((^[x]?\d+)\s?[x]\s?)", "", unify_price)
        no_sym = re.sub(r"[^\w\s.+]", "", no_quantity)
        stripped = no_sym.split(price, 1)[0]
        df.loc[index, "product"] = stripped.strip()
    return df


def prd2(data):
    df = ai(data)
    for index, row in df.iterrows():
        product = re.sub("\s+|  \t+", " ", row["deal"]).strip()
        stripped = product.split("/", 1)[0]
        stripped = re.sub(r"[^\w\s.+]", "", stripped)
        df.loc[index, "product"] = stripped.strip()
    return df
