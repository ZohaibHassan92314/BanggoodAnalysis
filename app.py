import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Banggood Dashboard", layout="wide", page_icon="📊")
st.title("📦 Banggood Products Analysis Dashboard")
st.markdown("Interactive dashboard showcasing insights on Banggood products data.")

# --- SQL Server Connection ---

server = r'DESKTOP-34R9A31\SQL2025Z'
database = 'BanggoodDB'
conn = pyodbc.connect(
f'DRIVER={{ODBC Driver 18 for SQL Server}};'
f'SERVER={server};'
f'DATABASE={database};'
f'Trusted_Connection=yes;'
f'Encrypt=no;'
)
df = pd.read_sql("SELECT * FROM dbo.BanggoodProducts", conn)

# --- Sidebar Filters ---

st.sidebar.header("Filters")
categories = df['main_category'].unique()
selected_category = st.sidebar.multiselect("Select Categories", categories, default=categories)
df_filtered = df[df['main_category'].isin(selected_category)]

# --- KPI Cards ---

col1, col2, col3, col4 = st.columns(4)
with col1:
 st.metric("Total Products", df_filtered.shape[0])
with col2:
 st.metric("Average Price", f"${df_filtered['price'].mean():.2f}")
with col3:
 st.metric("Average Rating", f"{df_filtered['rating'].mean():.2f}")
with col4:
 st.metric("Average Reviews", f"{df_filtered['review_count'].mean():.0f}")

# --- Price Distribution per Category ---

st.subheader("💰 Price Distribution per Category")
fig1, ax1 = plt.subplots(figsize=(10,5))
sns.boxplot(x='main_category', y='price', data=df_filtered, ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# --- Rating vs Price Scatter ---

st.subheader("⭐ Rating vs Price Scatter Plot")
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.scatterplot(data=df_filtered, x='price', y='rating', hue='main_category', alpha=0.7, ax=ax2)
st.pyplot(fig2)

# --- Top 5 Reviewed Products per Category ---

st.subheader("🏆 Top 5 Reviewed Products per Category")
top_reviewed = df_filtered.sort_values(['main_category','review_count'], ascending=[True, False])
st.dataframe(top_reviewed.groupby('main_category').head(5))

# --- Product Count per Category ---

st.subheader("📊 Product Count per Category")
count_cat = df_filtered['main_category'].value_counts().reset_index()
count_cat.columns = ['main_category','product_count']
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.barplot(x='main_category', y='product_count', data=count_cat, ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# --- Average Rating per Category ---

st.subheader("⭐ Average Rating per Category")
avg_rating = df_filtered.groupby('main_category')['rating'].mean().reset_index()
fig4, ax4 = plt.subplots(figsize=(10,5))
sns.barplot(x='main_category', y='rating', data=avg_rating, ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# --- Average Price per Category ---

st.subheader("💵 Average Price per Category")
avg_price = df_filtered.groupby('main_category')['price'].mean().reset_index()
fig5, ax5 = plt.subplots(figsize=(10,5))
sns.barplot(x='main_category', y='price', data=avg_price, ax=ax5)
plt.xticks(rotation=45)
st.pyplot(fig5)

st.markdown("---")
st.markdown("Dashboard created by **Zohaib Khan** | Powered by Streamlit & Python")
