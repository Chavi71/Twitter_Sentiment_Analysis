# topic_modeling.py
import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

STOP = set(stopwords.words("english"))

def preprocess_texts(texts):
    docs = []
    for t in texts:
        tokens = [w.lower() for w in word_tokenize(t) if w.isalpha()]
        tokens = [w for w in tokens if w not in STOP and len(w) > 2]
        docs.append(tokens)
    return docs

def compute_lda_topics(texts, num_topics=6):
    docs = preprocess_texts(texts)
    dictionary = corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10, random_state=42)
    topics = lda.print_topics(num_words=6)
    return topics, lda, dictionary, corpus
