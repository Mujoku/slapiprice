import pandas as pd


def msg_blocks(df, tid):
    blocks = []
    for index, row in df.iterrows():
        product = row["product"]
        price = row["prices"]
        supplier = row["supplier"]
        date = row["date"]
        currency = row["currency"]
        deal = [f"_*{product}*_\n_{date} | {supplier} | {price} {currency}_\n"]

        if index < 10:
            blocks = blocks + deal
        else:
            pass

    context = f""

    for v in blocks:
        context = context + v
    return context
