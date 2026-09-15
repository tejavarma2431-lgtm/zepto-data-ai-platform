# Data Pipeline

## Overview

This module scrapes book data from Books to Scrape, cleans the data, converts prices from GBP to INR, stores the data in a normalized SQLite database, and demonstrates SQL and pandas-based analysis.

## 1. Web Scraping

Source:

https://books.toscrape.com/

The scraper processes the first 5 paginated All Products pages.

A total of 100 books were scraped. After removing 5 rows where the category could not be parsed correctly, 95 books remained.

The following fields were collected:

- title
- price_gbp
- rating
- in_stock
- category

## 2. Data Cleaning

The following transformations were performed:

- Converted price from text to float.
- Converted star ratings from text to integer values from 1 to 5.
- Converted availability into a Boolean `in_stock` field.
- Removed rows where the category could not be parsed.
- Converted GBP prices to INR using the required fixed conversion rate:

`1 GBP = 105.50 INR`

The final dataset is stored in:

`books_cleaned.csv`

## 3. SQLite Database

The cleaned data is stored in:

`books.db`

The database contains two normalized tables:

### categories

- `category_id` - Primary Key
- `category_name` - Unique category name

### books

- `book_id` - Primary Key
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id` - Foreign Key referencing `categories.category_id`

The database is created by:

`database.py`

## 4. SQL Queries

Five SQL queries are implemented in:

`queries.py`

They demonstrate:

1. SELECT and WHERE
2. ORDER BY and LIMIT
3. DISTINCT, IN and JOIN
4. BETWEEN and ORDER BY
5. JOIN, IN and ORDER BY

The query outputs are saved as CSV files in:

`query_outputs/`

## 5. Pandas SQL Integration

The SQL results are loaded using:

`pd.read_sql()`

The JOIN operation is also reproduced using:

`pd.merge()`

The pandas merge result is saved as:

`query_outputs/pandas_merge_output.csv`

## Files

- `scraper.py` - Web scraping and cleaning
- `database.py` - SQLite database creation
- `queries.py` - SQL queries and pandas merge
- `books_cleaned.csv` - Cleaned scraped dataset
- `books.db` - SQLite database
- `query_outputs/` - Saved query and pandas outputs