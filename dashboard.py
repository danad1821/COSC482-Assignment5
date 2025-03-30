import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("My Dashboard")
st.write("Hello, Streamlit!")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_ebay_deals.csv")
    return df

df = load_data()

# Initialize session state for keywords
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []

st.sidebar.header("Filters")
hour_range = st.sidebar.slider("Select Hour", 0, 23, (0, 23))
df["timestamp"] = pd.to_datetime(df["timestamp"])
df_filtered = df[(df["timestamp"].dt.hour >= hour_range[0]) & (df["timestamp"].dt.hour <= hour_range[1])]
max_price = df["price"].max()
min_price = df["price"].min()
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, max_price))
df_filtered = df_filtered[(df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]

def clear_text():
    st.session_state["keywords"].append(st.session_state["keyword_input"].lower())
    st.session_state["keyword_input"] = ''

keyword = st.sidebar.text_input("Keyword", key="keyword_input")

if st.sidebar.button("Add keyword", on_click=clear_text):
    pass #clear text function will handle the changes.

col1, col2 = st.columns(2)

with col1:
    st.subheader("Deals Per Hour")
    deals_per_hour = df_filtered["timestamp"].dt.hour.value_counts().sort_index()
    fig1, ax1 = plt.subplots()
    ax1.bar(deals_per_hour.index, deals_per_hour.values)
    ax1.set_ylabel('Number of Deals')
    ax1.set_xlabel('Hour')
    st.pyplot(fig1)

with col2:
    st.subheader("Price Distribution")
    fig2, ax2 = plt.subplots()
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Price')
    counts, bins = np.histogram(df_filtered['price'])
    ax2.hist(bins[:-1], bins, weights=counts)
    st.pyplot(fig2)

with st.container():
    st.subheader("Keyword Frequency")
    if st.session_state["keywords"]:
        counts = []
        for key in st.session_state["keywords"]:
            counts.append(df_filtered['title'].str.lower().str.contains(key, na=False).sum())
        fig3, ax3 = plt.subplots()
        ax3.bar(st.session_state["keywords"], counts)
        ax3.set_ylabel('Count')
        ax3.set_xlabel('Keywords')
        st.pyplot(fig3)
    else:
        st.write("no keywords added")

with st.container():
    st.subheader("Summary Statistics")
    st.write(df_filtered.describe())

with st.expander("Show Full Dataset"):
    st.dataframe(df_filtered)