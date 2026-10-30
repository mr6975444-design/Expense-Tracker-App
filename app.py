
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# CUSTOM CSS DESIGN
# --------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #F8F7FF, #FDF2F8);
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #6D28D9;
    font-weight: 800;
}

h2, h3 {
    color: #5B21B6;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EDE9FE, #FCE7F3);
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #DDD6FE, #FBCFE8);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #C4B5FD;
    box-shadow: 0 4px 12px rgba(109,40,217,0.10);
}

[data-testid="stMetricLabel"] {
    color: #581C87;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    color: #4C1D95;
    font-weight: 800;
}

.stButton button {
    background: linear-gradient(90deg, #7C3AED, #EC4899);
    color: white;
    border-radius: 10px;
    border: none;
}

.stDownloadButton button {
    background: linear-gradient(90deg, #7C3AED, #EC4899);
    color: white;
    border-radius: 10px;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #8B5CF6, #EC4899);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# LOAD DATA
# --------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/cleaned_expenses.csv",
        parse_dates=["Date"]
    )
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Please run the data generation and cleaning programs first.")
    st.stop()


# --------------------------------
# DASHBOARD HEADER
# --------------------------------

st.title("💰 Personal Expense Tracker")

st.markdown(
    "### ✨ Smart Financial Analysis Dashboard"
)

st.caption(
    "Track your income, analyze expenses and monitor your budget."
)

st.divider()


# --------------------------------
# SIDEBAR FILTERS
# --------------------------------

st.sidebar.title("🎨 Dashboard Controls")
st.sidebar.markdown("### Filter Transactions")

categories = ["All"] + sorted(
    df["Category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "📂 Select Category",
    categories
)

selected_type = st.sidebar.selectbox(
    "💳 Transaction Type",
    ["All", "Income", "Expense"]
)

years = sorted(df["Year"].dropna().unique().tolist())

selected_year = st.sidebar.selectbox(
    "📅 Select Year",
    ["All"] + years
)

st.sidebar.divider()

st.sidebar.info(
    "Use these filters to explore your financial transactions."
)


# --------------------------------
# APPLY FILTERS
# --------------------------------

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type"] == selected_type
    ]

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]


# --------------------------------
# FINANCIAL CALCULATIONS
# --------------------------------

income_df = filtered_df[
    filtered_df["Type"] == "Income"
]

expense_df = filtered_df[
    filtered_df["Type"] == "Expense"
]

total_income = income_df["Amount"].sum()

total_expenses = expense_df["Amount"].sum()

balance = total_income - total_expenses


# --------------------------------
# FINANCIAL SUMMARY CARDS
# --------------------------------

st.subheader("📊 Financial Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💚 Total Income",
        value=f"₹{total_income:,.0f}"
    )

with col2:
    st.metric(
        label="❤️ Total Expenses",
        value=f"₹{total_expenses:,.0f}"
    )

with col3:
    st.metric(
        label="💜 Net Balance",
        value=f"₹{balance:,.0f}"
    )

st.divider()


# --------------------------------
# BUDGET MONITORING
# --------------------------------

st.subheader("🎯 Monthly Budget Monitoring")

monthly_budget = st.number_input(
    "Enter your monthly expense budget (₹)",
    min_value=0,
    value=20000,
    step=1000
)

if not expense_df.empty:

    monthly_expenses = expense_df.groupby(
        "Month_Year"
    )["Amount"].sum()

    latest_month = monthly_expenses.index.max()

    latest_expense = monthly_expenses.loc[
        latest_month
    ]

    st.write(f"📅 Latest month: **{latest_month}**")

    st.write(
        f"Monthly expenses: **₹{latest_expense:,.0f}**"
    )

    if monthly_budget > 0:

        budget_percentage = (
            latest_expense / monthly_budget
        )

        st.progress(
            min(budget_percentage, 1.0)
        )

        st.write(
            f"Budget used: {budget_percentage * 100:.1f}%"
        )

        if latest_expense > monthly_budget:
            st.error("⚠️ Monthly budget exceeded!")

        elif latest_expense == monthly_budget:
            st.warning("You have reached your budget limit.")

        else:
            st.success("🎉 You are within your monthly budget!")

else:
    st.info("No expense transactions available.")

st.divider()


# --------------------------------
# CATEGORY-WISE EXPENSE CHART
# --------------------------------

st.subheader("📂 Expense Analysis")

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### 🌈 Category-wise Expenses")

    if not expense_df.empty:

        category_data = expense_df.groupby(
            "Category"
        )["Amount"].sum().sort_values(
            ascending=False
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        category_data.plot(
            kind="bar",
            ax=ax,
            color=[
                "#8B5CF6",
                "#EC4899",
                "#06B6D4",
                "#F59E0B",
                "#10B981",
                "#6366F1",
                "#F97316"
            ]
        )

        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Expenses by Category")

        ax.set_facecolor("#F8F7FF")
        fig.patch.set_facecolor("#F8F7FF")

        plt.xticks(rotation=35)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No category expense data available.")


# --------------------------------
# MONTHLY EXPENSE TREND
# --------------------------------

with col2:

    st.markdown("#### 📈 Monthly Expense Trend")

    if not expense_df.empty:

        monthly_data = expense_df.groupby(
            "Month_Year"
        )["Amount"].sum()

        fig, ax = plt.subplots(figsize=(8, 5))

        monthly_data.plot(
            kind="line",
            marker="o",
            color="#8B5CF6",
            linewidth=3,
            markersize=7,
            ax=ax
        )

        ax.fill_between(
            range(len(monthly_data)),
            monthly_data.values,
            color="#C4B5FD",
            alpha=0.25
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Monthly Expense Trend")

        ax.set_facecolor("#F8F7FF")
        fig.patch.set_facecolor("#F8F7FF")

        plt.xticks(
            range(len(monthly_data)),
            monthly_data.index,
            rotation=45
        )

        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No monthly expense data available.")


st.divider()


# --------------------------------
# PAYMENT METHOD PIE CHART
# --------------------------------

st.subheader("💳 Payment Method Analysis")

if not expense_df.empty:

    payment_data = expense_df.groupby(
        "Payment_Method"
    )["Amount"].sum()

    fig, ax = plt.subplots(figsize=(7, 5))

    payment_data.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=[
            "#8B5CF6",
            "#EC4899",
            "#06B6D4",
            "#F59E0B"
        ],
        wedgeprops={"edgecolor": "white"}
    )

    ax.set_ylabel("")
    ax.set_title("Expenses by Payment Method")

    fig.patch.set_facecolor("#F8F7FF")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("No payment method data available.")


st.divider()


# --------------------------------
# TRANSACTION HISTORY
# --------------------------------

st.subheader("🧾 Transaction History")

st.write(
    f"Total transactions displayed: **{len(filtered_df)}**"
)

st.dataframe(
    filtered_df.sort_values(
        "Date",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# DOWNLOAD CSV
# --------------------------------

st.subheader("📥 Download Your Data")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Transactions CSV",
    data=csv,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#7C3AED;">
        <h4>💜 Expense Tracker Dashboard</h4>
        <p>Built with Python, Pandas, NumPy, Matplotlib and Streamlit</p>
        <p>Data Science Project | 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)
