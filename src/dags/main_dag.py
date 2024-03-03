"""
### DAG CryptoGraph ETL
This DAG is demonstrating an Extract -> Transform -> Load pipeline
"""
from __future__ import annotations

# [START import_module]
import json
from datetime import timedelta
from textwrap import dedent

import pendulum
import pymongo
import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

# [END import_module]

# [START instantiate_dag]
with DAG(
    "CryptoGraphETL",
    # [START default_args]
    default_args={
        "retries": 2,
        "owner": "cryptograph",
        "retry_delay": timedelta(minutes=1),
    },
    # [END default_args]
    description="DAG for extracting crypto price API and store to MongoDB",
    schedule="30 21 * * *",
    start_date=pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    catchup=False,
    is_paused_upon_creation=True,
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs["ti"]

        base_url = "https://api.coingecko.com/api/v3"
        endpoint_coins_markets = "/coins/markets"

        params_coins_markets = {
            "vs_currency": "usd",
            "ids": "bitcoin",
        }

        # data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        # ti.xcom_push("order_data", data_string)

        request_url = base_url + endpoint_coins_markets
        print(request_url)

        r = requests.get(request_url, params=params_coins_markets)
        pretty_json = json.loads(r.text)
        res_json = pretty_json[0]

        print(res_json)

        ti.xcom_push("crypto_data", res_json)

    # [END extract_function]

    # [START transform_function]
    # def transform(**kwargs):
    #     ti = kwargs["ti"]
    #     extract_data_string = ti.xcom_pull(task_ids="extract", key="order_data")
    #     order_data = json.loads(extract_data_string)

    #     total_order_value = 0
    #     for value in order_data.values():
    #         total_order_value += value

    #     total_value = {"total_order_value": total_order_value}
    #     total_value_json_string = json.dumps(total_value)
    #     ti.xcom_push("total_order_value", total_value_json_string)

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        ti = kwargs["ti"]

        # total_value_string = ti.xcom_pull(task_ids="transform", key="total_order_value")
        # total_order_value = json.loads(total_value_string)

        crypto_data = ti.xcom_pull(task_ids="extract", key="crypto_data")

        MONGO_USERNAME = Variable.get("cgetl_mongo_username")
        MONGO_PASSWORD = Variable.get("cgetl_mongo_password")

        client = pymongo.MongoClient(
            "mongodb+srv://{}:{}@cryptofolio.ur3en.mongodb.net/".format(
                MONGO_USERNAME, MONGO_PASSWORD
            )
        )
        print(client)

        db = client["CryptoGraph"]
        collection = db["BTC"]

        print("crypto:")
        print(type(crypto_data))
        print(crypto_data)

        insert_col = collection.insert_one(crypto_data)

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    # transform_task = PythonOperator(
    #     task_id="transform",
    #     python_callable=transform,
    # )
    # transform_task.doc_md = dedent(
    #     """\
    # #### Transform task
    # A simple Transform task which takes in the collection of order data from xcom
    # and computes the total order value.
    # This computed value is then put into xcom, so that it can be processed by the next task.
    # """
    # )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> load_task

# [END main_flow]

# [END tutorial]
