"""
Sales Performance & Territory Analysis
Dataset: Sample - Superstore.csv (Kaggle "Superstore Dataset")
Run:  python analysis.py
Output: printed findings + charts saved in the charts/ folder
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "Sample - Superstore.csv"
os.makedirs("charts", exist_ok=True)

# ---------- 1. Load and clean ----------
df = pd.read_csv(DATA_FILE, encoding="latin-1")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df = df.dropna(subset=["Order Date"])
df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["Year"] = df["Order Date"].dt.year

print("Rows:", len(df))
print("Total Sales: {:,.0f}".format(df["Sales"].sum()))
print("Total Profit: {:,.0f}".format(df["Profit"].sum()))
print("Overall Profit Margin: {:.1f}%".format(df["Profit"].sum() / df["Sales"].sum() * 100))

# ---------- 2. Region performance (territory analysis) ----------
region = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
region["Margin %"] = region["Profit"] / region["Sales"] * 100
region = region.sort_values("Sales", ascending=False)
print("\n--- Region performance ---")
print(region.round(1))

ax = region["Sales"].plot(kind="bar", color="#2E75B6", figsize=(7, 4))
ax.set_title("Sales by Region")
ax.set_ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/sales_by_region.png", dpi=120)
plt.close()

# ---------- 3. Category and sub-category ----------
sub = df.groupby(["Category", "Sub-Category"]).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
sub["Margin %"] = sub["Profit"] / sub["Sales"] * 100
sub = sub.sort_values("Profit")
print("\n--- 5 least profitable sub-categories ---")
print(sub.head(5).round(1))
print("\n--- 5 most profitable sub-categories ---")
print(sub.tail(5).round(1))

colors = ["#C00000" if p < 0 else "#548235" for p in sub["Profit"]]
ax = sub["Profit"].plot(kind="barh", color=colors, figsize=(8, 7))
ax.set_title("Profit by Sub-Category (red = loss-making)")
ax.set_xlabel("Profit")
plt.tight_layout()
plt.savefig("charts/profit_by_subcategory.png", dpi=120)
plt.close()

# ---------- 4. Monthly sales trend ----------
monthly = df.groupby("Month")["Sales"].sum()
ax = monthly.plot(figsize=(9, 4), color="#2E75B6", marker="o", markersize=3)
ax.set_title("Monthly Sales Trend")
ax.set_ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=120)
plt.close()

best_month = monthly.groupby(monthly.index.month).mean().idxmax()
print("\nStrongest month on average (1=Jan ... 12=Dec):", best_month)

# ---------- 5. Discount vs profit ----------
df["Discount Band"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0, 0.2, 0.4, 1],
    labels=["No discount", "Up to 20%", "21-40%", "Above 40%"],
)
disc = df.groupby("Discount Band", observed=True).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
disc["Margin %"] = disc["Profit"] / disc["Sales"] * 100
print("\n--- Discount vs profit ---")
print(disc.round(1))

ax = disc["Margin %"].plot(kind="bar", color="#ED7D31", figsize=(7, 4))
ax.set_title("Profit Margin by Discount Band")
ax.set_ylabel("Profit Margin %")
ax.axhline(0, color="black", linewidth=0.8)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/discount_vs_margin.png", dpi=120)
plt.close()

# ---------- 6. State level: where growth is being lost ----------
state = df.groupby("State").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
print("\n--- 5 loss-making states ---")
print(state.sort_values("Profit").head(5).round(0))

print("\nDone. Charts saved in the charts/ folder.")
