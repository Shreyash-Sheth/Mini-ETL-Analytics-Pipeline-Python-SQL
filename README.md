# Mini-ETL-Analytics-Pipeline-Python-SQL

## Project Overview
This mini-project demonstrates how Python and SQL can be combined to build a lightweight ETL (Extract, Transform, Load) workflow and generate actionable business insights from raw data. Using an open Online Retail dataset, the project highlights the benefits of structured data pipelines for quick analytics.

The workflow focuses on data cleaning, transformation, loading into SQLite, and SQL-based aggregation and ranking, followed by simple visualizations in Python. The goal is to show how Python + SQL can streamline analysis, even with small datasets, making insights accessible in minutes.

## Features

- ETL with Python:
    - Extract raw Excel dataset
    - Transform: clean columns, handle missing values, create new metrics (total_value)
    - Load into SQLite database

- SQL Queries:
    - Top 10 countries by total revenue
    - Monthly revenue trends globally
    - Monthly revenue trend in Ireland
    - Top 10 products by revenue in Ireland

- Python Visualisations:
    - Line chart for monthly revenue in Ireland
    - Horizontal bar chart for the top 10 products in Ireland
    - Optional display of tables directly from SQL queries

- Tools Used:
    - Python (pandas, matplotlib, sqlite3)
    - SQLite for structured storage and querying
    - Jupyter Notebook for development and visualisation

## Dataset

The dataset used is publicly available from the UCI Machine Learning Repository:

Online Retail Dataset: https://archive.ics.uci.edu/ml/datasets/Online+Retail

The dataset contains retail transactions from a UK-based online store, including InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country.

> For demonstration purposes, this project focuses on transactions from Ireland, but the workflow is fully adaptable to other countries or datasets.

## Code
```
# Step 1: Load dataset
file_path = "C:\\Users\\Desktop\\Project\\Retail_SQL_Python\\Online Retail.xlsx"
raw = pd.read_excel(file_path)

print("Columns in dataset:", raw.columns.tolist())

# Step 2: Rename columns for consistency
raw = raw.rename(columns={
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country"
})

# Step 3: Clean data
raw["invoice_date"] = pd.to_datetime(raw["invoice_date"], errors="coerce")
raw = raw.dropna(subset=["invoice_no", "customer_id"])  # drop missing values
raw = raw[raw["quantity"] > 0]  # remove cancellations
raw = raw[raw["unit_price"] > 0]

# Step 4: Create new metrics
raw["total_value"] = raw["quantity"] * raw["unit_price"]

# Step 5: Load into SQLite
conn = sqlite3.connect("retail.db")
raw.to_sql("transactions", conn, if_exists="replace", index=False)

# Step 6: Run SQL queries on the cleaned dataset
query1 = """
SELECT country, ROUND(SUM(total_value),2) as revenue
FROM transactions
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;
"""
top_countries = pd.read_sql(query1, conn)

query2 = """
SELECT strftime('%Y-%m', invoice_date) as month, ROUND(SUM(total_value),2) as revenue
FROM transactions
GROUP BY month
ORDER BY month;
"""
monthly_revenue = pd.read_sql(query2, conn)

conn.close()

print("\nTop 10 Countries by Revenue:")
print(top_countries)

print("\nMonthly Revenue Trend:")
print(monthly_revenue)
```

<img width="226" height="431" alt="Top Country and monthly revenue" src="https://github.com/user-attachments/assets/cf195b79-f22d-42a3-ba82-9733f54675c5" />


```
import matplotlib.pyplot as plt

# Reconnect to SQLite
conn = sqlite3.connect("retail.db")

# 1A. Monthly revenue for Ireland
query_ireland_monthly = """
SELECT strftime('%Y-%m', invoice_date) as month, 
       ROUND(SUM(total_value),2) as revenue
FROM transactions
WHERE country = 'EIRE'
GROUP BY month
ORDER BY month;
"""
ireland_monthly = pd.read_sql(query_ireland_monthly, conn)

# 1B. Top 10 products by revenue in Ireland
query_ireland_products = """
SELECT description, ROUND(SUM(total_value),2) as revenue
FROM transactions
WHERE country = 'EIRE'
GROUP BY description
ORDER BY revenue DESC
LIMIT 10;
"""
ireland_products = pd.read_sql(query_ireland_products, conn)

conn.close()

# 2A. Line chart for monthly revenue in Ireland
plt.figure(figsize=(10,5))
plt.plot(ireland_monthly["month"], ireland_monthly["revenue"], marker="o", linestyle="-")
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend in Ireland", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
```
<img width="989" height="490" alt="Revenue Trend" src="https://github.com/user-attachments/assets/f3d79309-b7ba-4d80-80f4-115feb069d8b" />


```
# 2B. Snapshot of top 10 products in Ireland
print("\nTop 10 Products by Revenue in Ireland:")
print(ireland_products)

plt.figure(figsize=(10,6))
plt.barh(ireland_products["description"], ireland_products["revenue"], color="skyblue")
plt.gca().invert_yaxis()  # highest at top
plt.title("Top 10 Products by Revenue in Ireland", fontsize=14)
plt.xlabel("Revenue (£)")
plt.tight_layout()
plt.show()
```

<img width="364" height="195" alt="Top 10 Products" src="https://github.com/user-attachments/assets/1c4642cd-218d-4d24-af6f-d6e188d79666" />
<img width="989" height="590" alt="Top 10 Products chart" src="https://github.com/user-attachments/assets/b5ac502b-fabe-4ccd-9af3-fe27d81a476e" />

## Insights

- Python makes ETL fast and reproducible, even for messy datasets.
- SQL enables powerful aggregation and ranking to extract meaningful business metrics.
- The combined workflow shows how small-scale pipelines can deliver actionable insights quickly:
  - Identify top-performing countries and products
  - Track monthly revenue trends
  - Easily extendable to other datasets, KPIs, or BI dashboards
