import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Banggood Products Dashboard", layout="wide")

st.title("📊 Banggood Products Dashboard")

# --- Load data ---

try:
import pyodbc
server = r'DESKTOP-34R9A31\SQL2025Z'
database = 'BanggoodDB'
conn = pyodbc.connect(
f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;Encrypt=no;'
)
df = pd.read_sql("SELECT * FROM dbo.BanggoodProducts", conn)
except:
st.warning("Local SQL Server not accessible. Using CSV fallback.")
df = pd.read_csv("BanggoodProducts.csv")

# --- Sidebar filters ---

categories = df['main_category'].unique()
selected_category = st.sidebar.selectbox("Select Main Category", categories)
df_filtered = df[df['main_category'] == selected_category]

# --- KPIs ---

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(df_filtered))
col2.metric("Avg Price", f"${df_filtered['price'].mean():.2f}")
col3.metric("Avg Rating", f"{df_filtered['rating'].mean():.2f}")
col4.metric("Avg Reviews", f"{df_filtered['review_count'].mean():.0f}")

# --- Price Distribution ---

st.subheader("Price Distribution")
fig, ax = plt.subplots()
sns.histplot(df_filtered['price'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# --- Rating vs Price Scatter ---

st.subheader("Rating vs Price")
fig2, ax2 = plt.subplots()
sns.scatterplot(x='price', y='rating', data=df_filtered, hue='review_count', size='review_count', sizes=(20,200), ax=ax2)
st.pyplot(fig2)

# --- Top 5 Reviewed Products ---

st.subheader("Top 5 Reviewed Products")
top5 = df_filtered.sort_values(by='review_count', ascending=False).head(5)
st.table(top5[['title', 'price', 'rating', 'review_count']])

# --- Product Count and Average Price per Subcategory ---

st.subheader("Subcategory Summary")
sub_summary = df_filtered.groupby('subcategory').agg({'title':'count','price':'mean','rating':'mean'}).reset_index()
sub_summary = sub_summary.rename(columns={'title':'Product Count','price':'Avg Price','rating':'Avg Rating'})
st.dataframe(sub_summary)
