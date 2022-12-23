from datetime import datetime as dt
from price_check import pc


def ai(data):
    """This function adds additional information to deals dataframe such as
    supplier name and time the deal was posted."""
    result = pc(data)
    result["supplier"] = data[0]
    return result
