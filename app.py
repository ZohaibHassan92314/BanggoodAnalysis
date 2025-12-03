import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Banggood Product Dashboard", layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("banggood_products_cleaned.csv")
    except:
        # Sample data if CSV missing
        np.random.seed(42)
        n = 200
        df = pd.DataFrame({
            "main_category": np.random.choice(["Phones", "Electronics", "Sports", "Lighting", "Tools"], n),
            "subcategory": np.random.choice(["Sub1","Sub2","Sub3"], n),
            "title": ["Product "+str(i) for i in range(n)],
            "price_usd": np.random.randint(5,500, n),
            "brand_name": np.random.choice(["BrandA","BrandB","BrandC"], n)
        })
        df["price_category"] = df["price_usd"].apply(lambda p: "Low" if p<20 else "Medium" if p<100 else "High")
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")
main_cat_filter = st.sidebar.multiselect("Select Main Category", options=df["main_category"].unique(), default=df["main_category"].unique())
price_filter = st.sidebar.multiselect("Select Price Category", options=df["price_category"].unique(), default=df["price_category"].unique())
brand_filter = st.sidebar.multiselect("Select Brand", options=df["brand_name"].unique(), default=df["brand_name"].unique())

# Apply filters
df_filtered = df[
    (df["main_category"].isin(main_cat_filter)) &
    (df["price_category"].isin(price_filter)) &
    (df["brand_name"].isin(brand_filter))
]

# ---------- KPI METRICS ----------
st.title("Banggood Products Dashboard")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(df_filtered))
col2.metric("Average Price (USD)", round(df_filtered["price_usd"].mean(),2))
col3.metric("Max Price (USD)", round(df_filtered["price_usd"].max(),2))
col4.metric("Min Price (USD)", round(df_filtered["price_usd"].min(),2))

# ---------- PLOTS ----------
st.markdown("---")
st.subheader("Price Distribution by Category")
fig1, ax1 = plt.subplots(figsize=(10,5))
sns.boxplot(x='price_category', y='price_usd', data=df_filtered, palette='Set2', ax=ax1)
ax1.set_xlabel("Price Category")
ax1.set_ylabel("Price (USD)")
st.pyplot(fig1)

st.subheader("Number of Products per Price Category")
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.countplot(x='price_category', data=df_filtered, order=df_filtered['price_category'].value_counts().index, palette='viridis', ax=ax2)
ax2.set_xlabel("Price Category")
ax2.set_ylabel("Count")
st.pyplot(fig2)

st.subheader("Top 10 Most Expensive Products")
top_exp = df_filtered.sort_values("price_usd", ascending=False).head(10)
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.barplot(x='price_usd', y='title', data=top_exp, palette='magma', ax=ax3)
ax3.set_xlabel("Price (USD)")
ax3.set_ylabel("Product")
st.pyplot(fig3)

st.subheader("Number of Products per Main Category")
fig4, ax4 = plt.subplots(figsize=(10,5))
sns.countplot(y='main_category', data=df_filtered, order=df_filtered['main_category'].value_counts().index, palette='coolwarm', ax=ax4)
st.pyplot(fig4)

st.subheader("Average Price per Main Category")
avg_price = df_filtered.groupby('main_category')['price_usd'].mean().reset_index().sort_values("price_usd", ascending=False)
fig5, ax5 = plt.subplots(figsize=(10,5))
sns.barplot(x='price_usd', y='main_category', data=avg_price, palette='cubehelix', ax=ax5)
ax5.set_xlabel("Average Price (USD)")
ax5.set_ylabel("Main Category")
st.pyplot(fig5)

# ---------- OPTIONAL: Show Table ----------
st.markdown("---")
st.subheader("Filtered Products Table")
st.dataframe(df_filtered.reset_index(drop=True))
