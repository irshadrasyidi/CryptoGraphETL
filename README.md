# CryptoGraphETL

This is an on-going personal project about observing, exploring, and analyzing the correlation between cryptocurrency prices and GPU prices.

## Background Story

In 2021, bitcoin price surged and reached a very significant level, creating euphoria in cryptocurrency space. Along with that, the price of GPU also rose really high, creating distraction in the gaming industry and communities. This fenomena can happen again as crypto industry is still growing and the needs of GPUs as bitcoin mining rig components are huge.

## Project Description

This repo contains 2 sub-projects:

1. Cryptocurrency price ETL
2. GPU price scrapper

### Cryptocurrency price ETL

This sub-project implements ETL of cryptocurrency prices, taken from [Coingecko API](https://www.coingecko.com/en/api) and loaded into GCP [Cloud Storage](https://cloud.google.com/storage) and [BigQuery](https://cloud.google.com/bigquery). The ETL job is deployed to a [Cloud Function](https://cloud.google.com/functions) and to make it run daily, we hit the function using [Cloud Scheduler](https://cloud.google.com/scheduler). On the end, data in BigQuery is read by [Looker Studio](https://lookerstudio.google.com/overview) to be shown on Looker Studio Dashboard.

<!-- TODO -->

Here is the architecture graph:

![CryptoGraphETL Architecture Diagram](https://github.com/irshadrasyidi/CryptoGraphETL/blob/main/assets/CryptoGraphETL.png?raw=true)

Here is the link to see the [dashboard](https://lookerstudio.google.com/reporting/1821f0d5-414d-4746-a371-983edc28da0b).

### GPU price scrapper

This other sub-project works on scrapping GPU prices from E-Commerce and GPU-related websites using Python and [Scrapy](https://scrapy.org/). The prices will be accumulated on daily basis, and stored in NoSQL database [MongoDB](https://www.mongodb.com/). There will be an ETL job to load the data from MongoDB to BigQuery as the main data warehouse. On the end, data in BigQuery will be read by Looker Studio to be shown on Dashboard.

Here is the architecture graph:

![CryptoGraphScrapper Architecture Diagram](https://github.com/irshadrasyidi/CryptoGraphETL/blob/main/assets/CryptoGraphScrapper.png?raw=true)
