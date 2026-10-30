
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned dataset
df = pd.read_csv("data/cleaned_expenses.csv")

# Create output folder
os.makedirs("outputs/charts", exist_ok=True)

# Separate income and expenses
expenses = df[df["Type"] == "Expense"]
income = df[df["Type"] == "Income"]

# 1. Calculate total income and expenses
total_income = income["Amount"].sum()
total_expenses = expenses["Amount"].sum()
balance = total_income - total_expenses

print("========== FINANCIAL SUMMARY ==========")
print("Total Income:", total_income)
print("Total Expenses:", total_expenses)
print("Net Balance:", balance)

# 2. Category-wise expense analysis
category_expenses = expenses.groupby("Category")["Amount"].sum()
category_expenses = category_expenses.sort_values(ascending=False)

print("\n========== CATEGORY-WISE EXPENSES ==========")
print(category_expenses)

# 3. Monthly expense analysis
monthly_expenses = expenses.groupby("Month_Year")["Amount"].sum()

print("\n========== MONTHLY EXPENSES ==========")
print(monthly_expenses)

# 4. Payment method analysis
payment_analysis = expenses.groupby("Payment_Method")["Amount"].sum()

print("\n========== PAYMENT METHOD ANALYSIS ==========")
print(payment_analysis)

# 5. Category-wise expense chart
plt.figure(figsize=(10, 6))
category_expenses.plot(kind="bar")
plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/category_expenses.png")
plt.close()

# 6. Monthly expense trend chart
plt.figure(figsize=(12, 6))
monthly_expenses.plot(kind="line", marker="o")
plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/monthly_expenses.png")
plt.close()

# 7. Payment method pie chart
plt.figure(figsize=(8, 8))
payment_analysis.plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Expenses by Payment Method")
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/charts/payment_methods.png")
plt.close()

print("\nAnalysis completed successfully!")
print("Charts saved in outputs/charts/")
