from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request
from flask_ngrok import run_with_ngrok
import time
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from collections import Counter
from heapq import nlargest
nlp = spacy.load('en_core_web_lg')
app = Flask(__name__)
run_with_ngrok(app)

# Spacy Summarize
def spacy_summarize(mytext):
    doc = nlp(mytext)
    keyword = []
    stop_words = set(stopwords.words('english'))
    pos_tag = ['PROPN','ADJ','NOUN','VERB']
    for token in doc:
        if(token.text in stop_words or token.is_punct):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
    final_sents = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sents)
    return summary

# # Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# # Fetch Text From Url
# def get_text(url):
# 	page = urlopen(url)
# 	soup = BeautifulSoup(page)
# 	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
# 	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = spacy_summarize(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

# @app.route('/analyze_url',methods=['GET','POST'])
# def analyze_url():
# 	start = time.time()
# 	if request.method == 'POST':
# 		raw_url = request.form['raw_url']
# 		rawtext = get_text(raw_url)
# 		final_reading_time = readingTime(rawtext)
# 		final_summary = text_summarizer(rawtext)
# 		summary_reading_time = readingTime(final_summary)
# 		end = time.time()
# 		final_time = end-start
# 	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

# @app.route('/comparer',methods=['GET','POST'])
# def comparer():
# 	start = time.time()
# 	if request.method == 'POST':
# 		rawtext = request.form['rawtext']
# 		final_reading_time = readingTime(rawtext)
# 		final_summary_spacy = text_summarizer(rawtext)
# 		summary_reading_time = readingTime(final_summary_spacy)
# 		# Gensim Summarizer
# 		final_summary_gensim = summarize(rawtext)
# 		summary_reading_time_gensim = readingTime(final_summary_gensim)
# 		# NLTK
# 		final_summary_nltk = nltk_summarizer(rawtext)
# 		summary_reading_time_nltk = readingTime(final_summary_nltk)
# 		# Sumy
# 		final_summary_sumy = sumy_summary(rawtext)
# 		summary_reading_time_sumy = readingTime(final_summary_sumy) 

# 		end = time.time()
# 		final_time = end-start
# 	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)



@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()