# Twitter Sentiment Analysis using NLP and NoSQL

An advanced **Twitter Sentiment Analysis System** that combines **Natural Language Processing (NLP)**, **Machine Learning**, and **NoSQL (MongoDB)** for analyzing public sentiment on Twitter in real-time.  
This project demonstrates how Big Data, NoSQL, and NLP can be integrated to extract meaningful insights and visualize trends from unstructured social media data.

---

## Table of Contents
- [Abstract](#abstract)
- [Objectives](#objectives)
- [System Architecture](#system-architecture)
- [Tools and Technologies](#tools-and-technologies)
- [Methodology](#methodology)
- [Results](#results)
- [Performance](#performance)
- [Conclusion](#conclusion)
 
---

## Abstract

The rise of social media platforms like Twitter has created a vast stream of unstructured textual data that reflects real-time public opinion.  
This project, **“Advanced NoSQL-Based Twitter Sentiment Analysis Using Natural Language Processing (NLP)”**, analyzes user sentiments on Twitter using a hybrid approach that integrates **Transformer-based models (RoBERTa)** with **NoSQL (MongoDB)**.  
Tweets are classified into **Positive**, **Negative**, or **Neutral** sentiments and visualized through an **interactive Streamlit dashboard** featuring sentiment distribution, time trends, topic modeling, and word clouds.

---

## Objectives

- Apply **Big Data Analytics** techniques to process and analyze large volumes of Twitter data.  
- Utilize **MongoDB (NoSQL)** for scalable, efficient tweet storage and querying.  
- Perform **Transformer-based sentiment classification** and **topic modeling**.  
- Visualize data insights using **interactive dashboards** built with Streamlit.  
- Enable **real-time querying** and exploration of sentiment trends.

---

## System Architecture

### 1. Data Ingestion
- Import tweets from datasets or Twitter API.  
- Clean and structure them into JSON format for MongoDB storage.

### 2. NoSQL Database Management
- Store tweets as documents in MongoDB collections.  
- Support filtering, aggregation, and indexing for fast querying.

### 3. Sentiment Analysis
- Clean tweets using NLP preprocessing.  
- Classify sentiments using **Transformer (RoBERTa)** and **VADER** analyzers.

### 4. Topic Modeling & Word Cloud
- Extract main topics using **Latent Dirichlet Allocation (LDA)**.  
- Generate **word clouds** to visualize frequent terms.

### 5. Visualization Dashboard
- Streamlit-based web interface with:
  - Pie charts for sentiment distribution  
  - Line charts for sentiment trends  
  - Hashtag frequency plots  
  - Word clouds & topic summaries

---

## Tools and Technologies

| Category | Tools Used |
|-----------|-------------|
| **Programming Language** | Python |
| **Libraries** | Pandas, NumPy, Transformers (Hugging Face), VADER Sentiment, Gensim, Matplotlib, Seaborn, Plotly, WordCloud, Streamlit |
| **Database** | MongoDB |
| **NLP Models** | RoBERTa (Transformer-based), VADER |
| **Visualization** | Streamlit |
| **IDE** | Visual Studio Code / Jupyter Notebook |
| **Version Control** | Git & GitHub |

---

## Methodology

1. **Data Collection** – Gather tweets via Twitter API or pre-existing datasets.  
2. **Database Storage** – Store cleaned tweets in MongoDB.  
3. **Query Input** – Allow users to enter keywords or hashtags.  
4. **Sentiment Analysis** – Process and classify each tweet as Positive, Negative, or Neutral.  
5. **Visualization** – Generate charts and analytics through Streamlit.  
6. **Output** – Display sentiment insights, trends, and downloadable results.

---

## Results 

- Processed over **5,000 tweets** related to chosen keywords or hashtags.  
- Generated real-time sentiment classifications and topic summaries.  

| Sentiment | Percentage |
|------------|-------------|
| Positive | 42% |
| Negative | 35% |
| Neutral | 23% |

---

## Performance
- Accuracy: ~91% on labeled Twitter datasets. 
- Latency: ~1s per batch sentiment analysis. 
- Scalability: Handles thousands of tweets via MongoDB efficiently.

---

**Key Visualizations:**
- Sentiment distribution (Pie Chart)  
- Temporal trends (Line Chart)  
- Word frequency (Word Cloud)  
- Top hashtags  
- Topic modeling insights

---


## Conclusion

This project demonstrates a complete **end-to-end sentiment analysis pipeline** integrating **NLP**, **Machine Learning**, and **NoSQL**.  
It efficiently processes and visualizes Twitter data to help researchers and businesses understand public opinion and emerging topics.  
The system’s modular design supports scalability, interactivity, and future extensions for real-time monitoring.


