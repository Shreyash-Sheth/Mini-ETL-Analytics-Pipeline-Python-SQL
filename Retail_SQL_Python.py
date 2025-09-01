#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pandas matplotlib


# In[2]:


import pandas as pd
import sqlite3

# Step 1: Load dataset
file_path = "C:\\Users\\Desktop\\Project\\Retail_SQL_Python\\Online Retail.xlsx"
raw = pd.read_excel(file_path)

print("Columns in dataset:", raw.columns.tolist())


# In[3]:


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


# In[4]:


# Step 3: Clean data
raw["invoice_date"] = pd.to_datetime(raw["invoice_date"], errors="coerce")
raw = raw.dropna(subset=["invoice_no", "customer_id"])  # drop missing values
raw = raw[raw["quantity"] > 0]  # remove cancellations
raw = raw[raw["unit_price"] > 0]


# In[5]:


# Step 4: Create new metrics
raw["total_value"] = raw["quantity"] * raw["unit_price"]


# In[6]:


# Step 5: Load into SQLite
conn = sqlite3.connect("retail.db")
raw.to_sql("transactions", conn, if_exists="replace", index=False)


# In[7]:


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


# In[8]:


import matplotlib.pyplot as plt

# Reconnect to SQLite
conn = sqlite3.connect("retail.db")


# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[13]:


# 2B. Snapshot of top 10 products in Ireland
print("\nTop 10 Products by Revenue in Ireland:")
print(ireland_products)


# In[14]:


# If you want a bar chart instead of table:
plt.figure(figsize=(10,6))
plt.barh(ireland_products["description"], ireland_products["revenue"], color="skyblue")
plt.gca().invert_yaxis()  # highest at top
plt.title("Top 10 Products by Revenue in Ireland", fontsize=14)
plt.xlabel("Revenue (£)")
plt.tight_layout()
plt.show()


# In[ ]:




