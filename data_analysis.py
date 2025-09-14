import pandas as pd
data=pd.read_excel('shopping_behavior_updated.xlsx')
data.head()
#print(data.describe())
sales_summary=data.groupby("Customer ID")["Purchase Amount (USD)"].sum()
#print(sales_summary)
top_spending_customers=sales_summary.idxmax()
top_purchase_amount=sales_summary.max()
print(f'Top spending customer ID: {top_spending_customers} with amount: {top_purchase_amount}')
#count how many items sold in each category
items_in_category=data['Category'].value_counts()
sold_items=data.groupby('Category')['Item Purchased'].value_counts()
print(sold_items)
#average purchase amount by gender
average_purchase=data.groupby("Gender")["Purchase Amount (USD)"].mean()
print(average_purchase)
