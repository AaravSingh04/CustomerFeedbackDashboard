import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

st.set_page_config(page_title="Customer Feedback Dashboard", layout="wide")

st.title("📊 Customer Feedback Dashboard")
st.write("Analyze customer feedback using Sentiment Analysis (TextBlob)")

# Store feedback during the session
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []

# Input Form
st.header("➕ Add Customer Feedback")

name = st.text_input("Customer Name")
feedback = st.text_area("Customer Feedback")

if st.button("Submit"):
    if name and feedback:
        polarity = TextBlob(feedback).sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        st.session_state.feedback_data.append({
            "Name": name,
            "Feedback": feedback,
            "Sentiment": sentiment
        })

        st.success("Feedback Added Successfully!")
    else:
        st.warning("Please fill all fields.")

# Display Feedback
if len(st.session_state.feedback_data) > 0:

    df = pd.DataFrame(st.session_state.feedback_data)

    st.header("📋 Feedback Records")
    st.dataframe(df, use_container_width=True)

    st.header("📈 Sentiment Distribution")

    sentiment_count = (
        df["Sentiment"]
        .value_counts()
        .reset_index()
    )
    sentiment_count.columns = ["Sentiment", "Count"]

    fig = px.bar(
        sentiment_count,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Customer Sentiment Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)
    