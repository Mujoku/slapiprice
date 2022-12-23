import pandas as pd


def match_deals(DB, double_check):

    products = DB.copy()
    grouped_data = match_strings(
        products["product"],
        double_check["product"],
        min_similarity=0.60,
        max_n_matches=10,
    )
    grouped_data.to_csv("testing.csv")
    column_names = ["deal", "prices", "supplier", "product", "date"]
    result = pd.DataFrame(columns=column_names)
    for i in grouped_data["left_index"]:
        res = DB.iloc[[i]]
        result = pd.concat([result, res], ignore_index=True, axis=0)
    return result
