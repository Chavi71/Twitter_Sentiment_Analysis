# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from mongoconnection import find_by_query_text, aggregate_sentiment_for_query, collection, ensure_indexes
from processing import analyze_text, MODEL_VERSION
from topic_modeling import compute_lda_topics
from datetime import datetime, timedelta
import numpy as np
from bson import ObjectId

st.set_page_config(layout="wide", page_title="Advanced NoSQL Twitter Sentiment")

ensure_indexes()

st.title("Advanced NoSQL Twitter Sentiment — Query-driven")

# Sidebar filters
st.sidebar.header("Filters")
query = st.sidebar.text_input("Keyword / Hashtag (leave blank = all)", value="")
days = st.sidebar.slider("Last N days", min_value=1, max_value=365, value=30)
limit = st.sidebar.slider("Max tweets to analyze", min_value=50, max_value=2000, value=500, step=50)

start_date = datetime.utcnow() - timedelta(days=days)
end_date = datetime.utcnow()

if st.sidebar.button("Run Analysis") or query:
    with st.spinner("Fetching tweets..."):
        docs = find_by_query_text(query, limit=limit, start_date=start_date, end_date=end_date)
    st.write(f"Found {len(docs)} tweets for query: `{query}`")

    # Analyze tweets (use cache where available)
    texts = []
    ids = []
    sentiments = []
    for d in docs:
        texts.append(d.get("text",""))
        ids.append(d.get("_id"))
    # batch analyze (simple loop)
    for txt, doc_id in zip(texts, ids):
        meta = analyze_text(txt, doc_id=doc_id, force=False)
        sentiments.append(meta["label"])

    df = pd.DataFrame({
        "text": texts,
        "sentiment": sentiments,
        "created_at": [d.get("created_at", None) for d in docs],
        "geo": [d.get("geo", None) for d in docs]
    })

    # Sentiment distribution
    st.subheader("Sentiment distribution for query")
    fig = px.pie(df, names="sentiment", title="Sentiment breakdown")
    st.plotly_chart(fig, use_container_width=True)

    # Time series sentiment
    st.subheader("Sentiment over time")
    df_ts = df.copy()
    df_ts["created_at"] = pd.to_datetime(df_ts["created_at"])
    df_ts = df_ts.set_index("created_at").resample("D").apply(lambda x: x.value_counts().get("sentiment", 0) if isinstance(x, pd.Series) else x.shape[0])
    # simpler approach: groupby date+sentiment
    df_dates = df.reset_index()
    df_dates["date"] = pd.to_datetime(df_dates["created_at"]).dt.date
    ts = df_dates.groupby(["date", "sentiment"]).size().reset_index(name="count")
    if not ts.empty:
        fig2 = px.line(ts, x="date", y="count", color="sentiment", markers=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Not enough data for time series.")

    # Wordcloud for the query
    st.subheader("Word Cloud (query)")
    words = " ".join(df["text"].tolist())
    if words.strip():
        wc = WordCloud(width=800, height=400, background_color="white").generate(words)
        plt.figure(figsize=(12,6))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.info("No words to show.")

    # Top hashtags
    st.subheader("Top hashtags")
    import re
    hashtags = []
    for t in df["text"]:
        hashtags += re.findall(r"#(\w+)", str(t))
    if hashtags:
        hc = pd.Series([h.lower() for h in hashtags]).value_counts().head(20)
        st.bar_chart(hc)
    else:
        st.info("No hashtags found.")

    # Topic Modeling (sample)
    st.subheader("Topic modeling (sample of tweets)")
    sample_texts = df["text"].dropna().tolist()[:200]
    if len(sample_texts) >= 10:
        topics, lda, dictionary, corpus = compute_lda_topics(sample_texts, num_topics=5)
        st.write("Detected topics:")
        for t in topics:
            st.write(t)
    else:
        st.info("Not enough data for topic modeling (need >=10 tweets).")

    # Show sample tweets
    st.subheader("Sample tweets")
    st.dataframe(df[["text","sentiment"]].head(20))

    # Download processed CSV
    #st.download_button("Download results as CSV", df.to_csv(index=False).encode('utf-8'), file_name="query_results.csv")
else:
    st.info("Enter a query or press 'Run Analysis' to start.")
