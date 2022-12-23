from natura import Finder
import pandas as pd
import re


def pc(data, default_currency="EUR"):
    """This function loops through arbitrary amount of deals in data passed as an argument and creates new
    dataframe with columns [deal, prices]"""
    data = list(filter(None, data))
    column_names = ["deal", "prices"]
    df = pd.DataFrame(columns=column_names)
    for deal in data:
        cleaned = re.sub(r"-\s*\d*$", "", deal)
        mf = Finder(converter=None, base_currency=default_currency)
        res = mf.findall(cleaned)
        check = mf.find(cleaned)
        if check:
            prices = []
            for v in res:
                price = f'{"{:.2f}".format(v.value) + " " + v.currency.upper()}'
                prices.append(price)
            s = ", ".join(prices)
            row = pd.DataFrame({"deal": deal, "prices": s}, index=[0])
            df = pd.concat([df, row], ignore_index=True, axis=0)
        else:
            pass
    return df
