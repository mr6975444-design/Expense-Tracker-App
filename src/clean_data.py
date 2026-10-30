
import pandas as pd
import os

# Load the dataset
df = pd.read_csv("data/expenses.csv")

print("Original Dataset Shape:", df.shape)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Create additional date columns
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year
df["Weekday"] = df["Date"].dt.day_name()
df["Month_Year"] = df["Date"].dt.to_period("M").astype(str)

# Save cleaned dataset
os.makedirs("data", exist_ok=True)
df.to_csv("data/cleaned_expenses.csv", index=False)

print("\nData cleaning completed successfully!")
print("Cleaned Dataset Shape:", df.shape)

print("\nCleaned Dataset Preview:")
print(df.head())
