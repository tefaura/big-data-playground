# big-data-playground

Data pipeline: ingest CSV from a source (e.g. GitHub URL), write raw CSV and curated Parquet to S3 (boto3).

## Install

```bash
pip install -r requirements.txt
```

## Main command

```bash
python scripts/get_data.py \
  --source "https://raw.githubusercontent.com/nbchambers95/data-science-projects/refs/heads/main/milkshake-forecasting/ItemSales_2023_2025.csv" \
  --raw-out "s3://aws-s3-tefaura-big-data-playground/raw-csv/sales.csv" \
  --curated-out "s3://aws-s3-tefaura-big-data-playground/curated-out/sales.parquet"
```

### Parameters

| Parameter       | Required | Description |
|----------------|----------|-------------|
| `--source`     | Yes      | CSV source (HTTP/HTTPS URL, e.g. GitHub raw link). |
| `--raw-out`    | No       | S3 path for raw CSV. Example: `s3://bucket/raw-csv/sales.csv` |
| `--curated-out`| No       | S3 path for curated Parquet. Example: `s3://bucket/curated-out/sales.parquet` |

**What it does:** Downloads the CSV from `--source`, uploads it as-is to `--raw-out` (S3), then reads that from S3, converts to Parquet, and uploads to `--curated-out` (S3). AWS credentials must be configured (e.g. `~/.aws/credentials` or env vars).
## Dataset

**Name:** ItemSales_2023_2025.csv  
**Source:** Public GitHub repository (POS sales export)  
**Domain:** Retail / Food & Beverage (Milkshake sales)  
**Data type:** Transactional (event-level POS data)  
**Period:** 2023–2025  

### Description
The dataset represents transactional sales data exported from a Point-of-Sale (POS) system.
Each record corresponds to the sale of a single item as part of a customer transaction.

The data includes timestamps, product information, sales metrics, transaction identifiers,
and contextual attributes such as location, channel, and dining option.

### Grain
**1 row = sale of a single item within a transaction at a specific timestamp and location.**

### Key fields
- **Time-related:** `Date`, `Time`, `Time Zone`
- **Product:** `Item`, `Category`, `SKU`
- **Sales metrics:** `Qty`, `Gross Sales`, `Discounts`, `Net Sales`, `Tax`
- **Transaction identifiers:** `Transaction ID`, `Payment ID`
- **Context:** `Location`, `Channel`, `Dining Option`

### Purpose
This dataset is used to simulate a real-world data engineering pipeline for retail transactional data.
The project focuses on:
- ingesting raw transactional data,
- transforming it into an analytics-friendly Parquet format,
- designing an S3-compatible data lake layout,
- and preparing the data for downstream analytical queries and time-based aggregations.
