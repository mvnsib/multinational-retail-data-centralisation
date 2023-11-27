# Multinational Retail Data Centralisation Project

## Table of Contents

- Project Title
- Table of Contents
- Description
- Installation Guide
- Usage Guide
- File Structure
- License Information

## Description

This project, assigned by AiCore as part of the Cloud Engineering pathway, focused on enhancing skills in data extraction and cleaning using Python. The primary objective was to gather and clean data from various sources, followed by uploading the processed data into a local PostgreSQL database. The subsequent steps involved designing a database schema using the star schema model. Finally, the data stored in the PostgreSQL database was queried to extract meaningful insights, thus demonstrating proficiency in data-driven analysis for the specified scenario.

## Installation Guide

To install this project, it's required to install the latest version of

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

- libraries used:
  - pandas
  - numpy
  - sqlalchemy
  - psycopg2
  - requests
  - tabula
  - json
  - boto3

## Usage Guide

1. Install all the packages listed in Installation Guide
2. Open the Terminal on your machine and type `python main.py`.
3. The program will extract all the data and upload it to the local PostgreSQL database
4. Open PGAdmin 4
5. Run the Schema Creation one by one from ms3.sql
6. To query the data run one by one from ms4.sql

## File Structure

```
📦 multinational-retail-data-centralisation
├─ extracted_data
│  ├─ card_details.pdf
│  ├─ dim_order.csv
│  ├─ dim_products.csv
│  ├─ dim_products_unclean.csv
│  └─ dim_store_data.csv
├─ data_cleaning.py
├─ database_utils.py
├─ data_extraction.py
├─ main.py
├─ ms3.sql
├─ ms4.sql
└─ README.md
```

## License Information

Github license\
AiCore license
