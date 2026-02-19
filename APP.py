import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(page_title="Canteen Dashboard", layout="wide")

# ==============================
# Arabic Font Fix
# ==============================

matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.rcParams['axes.unicode_minus'] = False

def arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ==============================
# Load Data from Google Sheet
# ==============================

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1R-_bDgdCnpS-7gmNlKz5cGAbFo7ugb1RZDXqGI5UB6M/export?format=csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# ==============================
# Data Processing
# ==============================

df['cost'] = df['quantity_sold'] * df['unit_cost']
df['revenue'] = df['quantity_sold'] * df['unit_price']
df['profit'] = df['revenue'] - df['cost']
df['date'] = pd.to_datetime(df['date'])
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
# Today Cards
# ==============================

st.subheader("Today Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Revenue Today", f"{df_today['revenue'].sum():,.0f}")
col2.metric("Cost Today", f"{df_today['cost'].sum():,.0f}")
col3.metric("Profit Today", f"{df_today['profit'].sum():,.0f}")

# ==============================
# Sales Trend
# ==============================

st.subheader("📈 Sales Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['date'], df['revenue'])
ax.set_xlabel(arabic_text("التاريخ"))
ax.set_ylabel(arabic_text("الإيراد"))
st.pyplot(fig)

# ==============================
# Product Analysis
# ==============================

df_group = df_month.groupby('product_name').agg(
    sales=('revenue', 'sum'),
    cost=('cost', 'sum'),
    profit=('profit', 'sum')
)

# Top 5
st.subheader("🔥 Top 5 Products by Sales")

top_5 = df_group.sort_values(by='sales', ascending=False).head()

fig1, ax1 = plt.subplots()
sns.barplot(x=top_5.index, y=top_5['sales'], ax=ax1)
ax1.set_title(arabic_text("أعلى 5 منتجات مبيعًا"))
ax1.set_xticklabels([arabic_text(i) for i in top_5.index], rotation=45)
st.pyplot(fig1)

# Bottom 5
st.subheader("📉 Bottom 5 Products by Sales")

bottom_5 = df_group.sort_values(by='sales', ascending=True).head()

fig2, ax2 = plt.subplots()
sns.barplot(x=bottom_5.index, y=bottom_5['sales'], ax=ax2)
ax2.set_title(arabic_text("أقل 5 منتجات مبيعًا"))
ax2.set_xticklabels([arabic_text(i) for i in bottom_5.index], rotation=45)
st.pyplot(fig2)

# Sales Share
st.subheader("📊 Products Sales Share")

fig3, ax3 = plt.subplots()
ax3.pie(df_group['sales'], labels=[arabic_text(i) for i in df_group.index], autopct='%0.2f%%')
st.pyplot(fig3)

# ==============================
# Show Data Table at End
# ==============================

st.subheader("📋 Data Table")

st.dataframe(df_month, use_container_width=True)
