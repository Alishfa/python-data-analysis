import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display


#2. Open the Dataset

DATA_DIR = "orders_raw.csv"

df = pd.read_csv(DATA_DIR)
print("Dataframe loaded successfully!")

display(df.head()) 
print(df.shape)
display(df.describe())
display(df.info())

#3. Check Data Quality
print("Checking for missing values and duplicates...")
display(df.isnull().sum())
print("duplicates in the dataset:")
display(df.duplicated().sum())
print("Data quality check completed.")


#unique values in region column and category column

print("Unique values in region column:")
print(df['region'].nunique())
print("Unique values in category column:")
print(df['category'].nunique())

#4. Data Cleaning
#create clean func
def clean_data(df):
    cleaned_df = df.copy()
    # Add cleaning logic here
    # 2. Strip currency symbols/spaces from unit_price before converting
    cleaned_df['unit_price'] = (
        cleaned_df['unit_price']
        .astype(str)
        .str.replace(r'[^0-9.-]', '', regex=True)
    )
    cleaned_df['region'] = cleaned_df['region'].str.strip().str.title()
    cleaned_df['category'] = cleaned_df['category'].str.strip().str.title()
    #convert order_date to datetime
    cleaned_df['order_date'] = pd.to_datetime(cleaned_df['order_date'], errors='coerce')
    # convert quantity, unit_price and order_value to numeric values.
    cleaned_df['quantity'] = pd.to_numeric(cleaned_df['quantity'], errors='coerce')
    cleaned_df['unit_price'] = pd.to_numeric(cleaned_df['unit_price'], errors='coerce')
    cleaned_df['order_value'] = pd.to_numeric(cleaned_df['order_value'], errors='coerce')
    #5. Remove Invalid Records
    # Remove rows with missing values in critical columns
    cleaned_df.drop_duplicates(inplace=True)
    cleaned_df = cleaned_df[
        cleaned_df['order_date'].notna()
        & cleaned_df['quantity'].notna()
        & cleaned_df['unit_price'].notna()
        & cleaned_df['order_value'].notna()
        & (cleaned_df['quantity'] > 0)
        & (cleaned_df['unit_price'] > 0)
        & (cleaned_df['order_value'] > 0)
    ].copy()
    return cleaned_df
#7. Save a Quality Report

def create_quality_report(raw_df, cleaned_df):
    report = {
        "Total Records": [len(raw_df), len(cleaned_df)],
        "Missing Values": [raw_df.isnull().sum().sum(), cleaned_df.isnull().sum().sum()],
        "Duplicates": [raw_df.duplicated().sum(), cleaned_df.duplicated().sum()],
        "Invalid Records Removed": [len(raw_df) - len(cleaned_df), 0]
    }
    return pd.DataFrame(report, index=["Raw Data", "Cleaned Data"])
quality_report = create_quality_report(df, clean_data(df))
display(quality_report)
#saving file to csv
os.makedirs("output", exist_ok=True)
quality_report.to_csv("output/quality_report.csv", index=False)
cleaned_df = clean_data(df)
cleaned_df.to_csv("output/cleaned_orders.csv", index=False)

#8. Explore the Cleaned Data
sales_by_region = (
    cleaned_df.groupby('region')['order_value']
    .sum()
    .sort_values(ascending=False)
      )
print("Sales by Region:")
display(sales_by_region)
category_count = cleaned_df['category'].value_counts()
print("Category Count:")
display(category_count)
mean_order_value = cleaned_df['order_value'].mean()
median_order_value = cleaned_df['order_value'].median()
print(f"Mean Order Value: {mean_order_value:.2f}")
print(f"Median Order Value: {median_order_value:.2f}")
std_order_value = cleaned_df['order_value'].std()
print(f"Standard Deviation of Order Value: {std_order_value:.2f}")

region_vs_category = pd.crosstab(cleaned_df['region'], cleaned_df['category'], values = cleaned_df['order_value'], aggfunc='sum', margins=True, margins_name="Total"  ).fillna(0)
print("Region vs Category Crosstab:")
display(region_vs_category)

#9. Visualize the Data
#histogram of ordervalues

plt.figure(figsize=(10, 6))
sns.histplot(cleaned_df['order_value'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Order Values')
plt.xlabel('Order Value')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("output/order_value_distribution.png")  
plt.show()
# Sales by Region Bar Plot
region_sales = cleaned_df.groupby("region", as_index=False)["order_value"].sum()
plt.figure(figsize=(10, 6))
sns.barplot(data=region_sales, x="region", y="order_value", palette="viridis")
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig("output/sales_by_region.png")
plt.show()

#scatterplot of order value versus delivery day

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data = cleaned_df,
    x = "delivery_day",
    y = "order_value",
    hue = "category",
)
plt.title('Order Value vs Delivery Day')
plt.xlabel('Delivery Day')
plt.ylabel  ('Order Value')
plt.tight_layout()  
plt.savefig("output/order_value_vs_delivery_day.png")
plt.show()



