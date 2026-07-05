import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import os

st.set_page_config(page_title="Customer Feedback Dashboard", layout="wide")

st.title("📊 Customer Feedback Dashboard")
st.write("Analyze customer feedback using Sentiment Analysis (TextBlob)")

CSV_FILE = "customer_feedback.csv"

# Load CSV
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Customer", "Feedback"])

# Add Sentiment Column
def get_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Feedback"].apply(get_sentiment)

# ---------- Add Feedback ----------
st.header("➕ Add Customer Feedback")

name = st.text_input("Customer Name")
feedback = st.text_area("Customer Feedback")

if st.button("Submit"):
    if name and feedback:

        new_row = pd.DataFrame({
            "Customer": [name],
            "Feedback": [feedback]
        })

        df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(CSV_FILE, index=False)

        st.success("Feedback Added Successfully!")
        st.rerun()

    else:
        st.warning("Please fill all fields.")

# ---------- Show Data ----------
st.header("📋 Feedback Records")
st.dataframe(df, use_container_width=True)

# ---------- Sentiment ----------
df["Sentiment"] = df["Feedback"].apply(get_sentiment)

st.header("📈 Sentiment Distribution")

sentiment_count = df["Sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Count"]

fig = px.bar(
    sentiment_count,
    x="Sentiment",
    y="Count",
    color="Sentiment",
    title="Customer Sentiment Analysis"
)

st.plotly_chart(fig, use_container_width=True)