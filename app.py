import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Banggood Dashboard", layout="wide")
st.title("📊 Banggood Products Dashboard")

# --- Load CSV safely ---

try:
 df = pd.read_csv("banggood_products_cleaned.csv")
except FileNotFoundError:
 st.error("CSV file not found!")
st.stop()

# --- Ensure numeric columns ---

for col in ['price','rating','review_count']:
 if col in df.columns:
  df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# --- Sidebar filter ---

if 'main_category' in df.columns:
 category = st.sidebar.selectbox("Select Main Category", df['main_category'].dropna().unique())
 df_filtered = df[df['main_category']==category]
else:
 df_filtered = df.copy()

# --- Simple KPIs ---

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df_filtered))
col2.metric("Avg Price", f"${df_filtered['price'].mean():.2f}" if 'price' in df_filtered else "N/A")
col3.metric("Avg Rating", f"{df_filtered['rating'].mean():.2f}" if 'rating' in df_filtered else "N/A")

# --- Chart 1: Price Distribution ---

if 'price' in df_filtered:
 st.subheader("Price Distribution")
fig, ax = plt.subplots()
sns.histplot(df_filtered['price'], bins=20, kde=True, color='skyblue', ax=ax)
st.pyplot(fig)

# --- Chart 2: Rating vs Price ---

if 'price' in df_filtered and 'rating' in df_filtered:
 st.subheader("Rating vs Price")
fig2, ax2 = plt.subplots()
sns.scatterplot(x='price', y='rating', data=df_filtered, hue='review_count' if 'review_count' in df_filtered else None, ax=ax2)
st.pyplot(fig2)
