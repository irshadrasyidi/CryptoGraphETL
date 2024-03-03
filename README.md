# CryptoGraphETL

This is an on-going personal project about exploring and analyzing the correlation between cryptocurrency prices and GPU prices.

## Background Story

In 2021, bitcoin price surged and reached a very significant level, creating euphoria in cryptocurrency space. Along with that, the price of GPU also rose really high, creating distraction in the gaming industry and communities. This fenomena can happen again as crypto industry is still growing and the needs of GPUs as bitcoin mining rig components are huge.

## Project Description

This repo contains 2 sub-projects:

1. Cryptocurrency price ETL
2. GPU price scrapper

### Cryptocurrency price ETL

This sub-project implements ETL of cryptocurrency prices, taken from [Coingecko API](https://www.coingecko.com/en/api) and loaded into GCP [Cloud Storage](https://cloud.google.com/storage) and [BigQuery](https://cloud.google.com/bigquery). The ETL job is deployed to a [Cloud Function](https://cloud.google.com/functions) and to make it run daily, we hit the function using [Cloud Scheduler](https://cloud.google.com/scheduler).

<!-- TODO -->

<!-- Here is the architecture graph: -->
