import json
from datetime import date

import pandas as pd
import pandas_gbq
import requests

# def get_price(request):
#     baseURL = "https://api.coingecko.com/api/v3"

#     endpoint_coins_markets = "/coins/markets"
#     params_coins_markets = {
#         "vs_currency": "usd",
#         "ids": "bitcoin,ethereum,binancecoin",
#     }

#     requestURL = baseURL + endpoint_coins_markets
#     r = requests.get(requestURL, params=params_coins_markets)

#     pretty_json = json.loads(r.text)

#     df = pd.json_normalize(pretty_json)

#     return None


def get_price(request):
    baseURL = "https://api.coingecko.com/api/v3"

    endpoint_coins_markets = "/coins/markets"
    params_coins_markets = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,binancecoin,ripple,solana,cardano,dogecoin,tron",
    }

    # EXTRACT
    # Get coin price via Coingecko API
    requestURL = baseURL + endpoint_coins_markets
    r = requests.get(requestURL, params=params_coins_markets)

    pretty_json = json.loads(r.text)
    df = pd.json_normalize(pretty_json)

    bucket_name = "cryptograph-etl"

    today = date.today()

    # Save raw data as CSV to GCS
    df.to_csv("gs://" + bucket_name + "/crypto/raw/raw_" + str(today) + ".csv")

    # TRANSFORM
    # Drop columns
    df_exclude = df.drop(
        columns=[
            "symbol",
            "name",
            "image",
            "roi",
            "roi.times",
            "roi.currency",
            "roi.percentage",
        ]
    )

    # Rename Columns
    df_exclude = df_exclude.rename(columns={"id": "coin_id"})

    df_split = []
    coin_list = ["btc", "eth", "bnb", "xrp", "sol", "ada", "doge", "trx"]

    # Split coins
    for row in df_exclude.index:
        temp_df = (df_exclude.iloc[row : row + 1]).reset_index(drop=True)
        temp_df.to_csv(
            "gs://"
            + bucket_name
            + "/crypto/processed/"
            + coin_list[row]
            + "/"
            + coin_list[row]
            + "_"
            + str(today)
            + ".csv"
        )
        df_split.append(temp_df)

    # Change data type
    df_exclude[["ath_date", "atl_date", "last_updated"]] = df_exclude[
        ["ath_date", "atl_date", "last_updated"]
    ].apply(pd.to_datetime)

    # LOAD
    # Load to BQ
    pandas_gbq.to_gbq(
        df_exclude,
        "CRYPTOGRAPH.crypto_price",
        project_id="forward-vector-396403",
        if_exists="append",
    )

    return "Done"
