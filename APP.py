import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Canteen Dashboard", layout="wide")

# ==============================
# Load Data from Google Sheet
# ==============================

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1R-_bDgdCnpS-7gmNlKz5cGAbFo7ugb1RZDXqGI5UB6M/export?format=csv"
    df = pd.read_csv(url)
    return df

try:
    df = load_data()

    # ==============================
    # Data Processing
    # ==============================

    df['date'] = pd.to_datetime(df['date'])
    df['cost'] = df['quantity_sold'] * df['unit_cost']
    df['revenue'] = df['quantity_sold'] * df['unit_price']
    df['profit'] = df['revenue'] - df['cost']
    df['month'] = df['date'].dt.month

    # ==============================
    # Sidebar Filter
    # ==============================

    st.sidebar.header("Filters")
    selected_month = st.sidebar.selectbox(
        "Select Month",
        sorted(df['month'].unique())
    )

    df_month = df[df['month'] == selected_month]
    today = pd.to_datetime(datetime.today().date())
    df_today = df[df['date'] == today]

    # ==============================
    # Title
    # ==============================

    st.title("📊 Canteen Sales Dashboard")

    # ==============================
    # Monthly Cards
    # ==============================

    st.subheader(f"Month {selected_month} Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"{df_month['revenue'].sum():,.0f}")
    col2.metric("Cost", f"{df_month['cost'].sum():,.0f}")
    col3.metric("Profit", f"{df_month['profit'].sum():,.0f}")

    # ==============================
    # Sales Trend
    # ==============================

    st.subheader("📈 Sales Trend")
    fig, ax = plt.subplots(figsize=(10, 5))
    # تجميع البيانات حسب التاريخ لرسم خط زمني صحيح
    daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
    ax.plot(daily_revenue['date'], daily_revenue['revenue'], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ... بقية الكود الخاص بالرسوم البيانية تعمل بشكل صحيح ...
    
except Exception as e:
    st.error(f"حدث خطأ في تحميل البيانات: {e}")
    st.info("تأكد من أن رابط Google Sheet متاح للجميع (Anyone with the link can view)")