
import pandas as pd
import numpy as np
import os

np.random.seed(42)

num_transactions = 1000

expense_categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare",
    "Education"
]

payment_methods = ["Cash", "UPI", "Credit Card", "Debit Card"]

# Generate transaction types first
transaction_types = np.random.choice(
    ["Income", "Expense"],
    num_transactions,
    p=[0.2, 0.8]
)

# Assign categories based on transaction type
categories = [
    "Salary" if transaction == "Income"
    else np.random.choice(expense_categories)
    for transaction in transaction_types
]

data = {
    "Date": pd.date_range(
        start="2025-01-01",
        periods=num_transactions,
        freq="D"
    ),
    "Category": categories,
    "Amount": np.random.randint(
        100, 10000,
        num_transactions
    ),
    "Type": transaction_types,
    "Payment_Method": np.random.choice(
        payment_methods,
        num_transactions
    ),
    "Description": [
        f"Transaction {i+1}"
        for i in range(num_transactions)
    ]
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_csv("data/expenses.csv", index=False)

print("Sample expense data generated successfully!")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nTransaction types:")
print(df["Type"].value_counts())
