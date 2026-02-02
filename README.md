# big-data-playground
The first pet project for Sasha.

## Project Overview

This project implements a **data engineering pipeline** for processing transactional sales data using a **data lake architecture**. The pipeline follows the principle of separating data into distinct layers: **raw** (unchanged source data) and **curated** (analytics-ready format).

### Core Idea

The pipeline implements a **two-layer data architecture**:

1. **Raw Layer** (`data/raw/`): Stores source data exactly as received, without any transformations. This preserves the original data for auditability and allows reprocessing if needed.

2. **Curated Layer** (`data/curated/`): Contains transformed, analytics-friendly data in Parquet format. Parquet provides:
   - **Compression**: Significantly smaller file sizes than CSV
   - **Columnar storage**: Optimized for analytical queries
   - **Type preservation**: Maintains data types efficiently
   - **Schema evolution**: Supports schema changes over time

### Pipeline Flow

```
Source (URL/S3/Local) → Raw Layer (CSV) → Curated Layer (Parquet)
```

The pipeline executes in a single command:
- Downloads/reads raw transactional data from a source
- Saves it unchanged to the raw layer (CSV format)
- Transforms it into Parquet format
- Saves it to the curated layer

**Key Design Principles:**
- **Single command execution**: All steps run with one command
- **No data in repository**: Data files are gitignored, keeping the repo lightweight
- **Flexible source**: Supports URLs, local paths, and S3-compatible sources
- **Reproducible**: Raw data can be reprocessed to curated layer at any time

## Install dependencies

```bash
pip install -r requirements.txt
```

## Scripts
### `scripts/get_data.py`

**Purpose:** Complete data ingestion and transformation pipeline. Downloads raw data, saves to raw layer, then transforms to curated Parquet format.

**Usage:**
```bash
python scripts/get_data.py --source <URL_OR_PATH> [--raw-out PATH] [--curated-out PATH]
```

**Arguments:**
- `--source` (required): Data source - can be:
  - HTTP/HTTPS URL: `https://example.com/data.csv`
  - Local file path: `data/raw/existing.csv`
  - S3 path: `s3://bucket/path/data.csv`
- `--raw-out` (optional): Output path for raw CSV layer. Default: `data/raw/dataset.csv`
- `--curated-out` (optional): Output path for curated Parquet layer. Default: `data/curated/dataset.parquet`

**Examples:**
```bash
# Basic usage with defaults
python scripts/get_data.py --source "https://raw.githubusercontent.com/nbchambers95/data-science-projects/refs/heads/main/milkshake-forecasting/ItemSales_2023_2025.csv"

# Custom output paths
python scripts/get_data.py --source "https://..." --raw-out "data/raw/sales.csv" --curated-out "data/curated/sales.parquet"

# From local file
python scripts/get_data.py --source "data/raw/existing.csv" --curated-out "data/curated/output.parquet"
```

**What it does:**
1. Downloads/reads the CSV from the source
2. Saves it unchanged to the raw layer (CSV format)
3. Transforms it to Parquet format
4. Saves it to the curated layer

---

### `scripts/view_parquet.py`

**Purpose:** Inspect and view contents of a Parquet file. Displays dataset statistics, sample rows, missing values, and column information.

**Usage:**
```bash
python scripts/view_parquet.py <PARQUET_FILE> [--rows N]
```

**Arguments:**
- `parquet_file` (required): Path to the Parquet file to view
- `--rows` (optional): Number of rows to display. Default: `5`

**Examples:**
```bash
# View with default 5 rows
python scripts/view_parquet.py data/curated/dataset.parquet

# View with 10 rows
python scripts/view_parquet.py data/curated/dataset.parquet --rows 10

# View any parquet file
python scripts/view_parquet.py data/curated/sales.parquet
```

**Output includes:**
- Dataset shape (rows, columns)
- First N rows (all columns visible)
- Missing values count per column
- Total row count
- All column names 



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
