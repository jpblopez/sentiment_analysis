import nltk
import re

from flask import request, Flask, jsonify
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

anal = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english')) 
tb = TreebankWordDetokenizer()
lm = WordNetLemmatizer()

app = Flask(__name__)
cors = CORS(app)

def cleaner(text):
    without_link = re.sub(r'( https?:\/\/\S*\s*)|#', ' ', text)
    without_html = re.sub(r'&[a-zA-Z]+;', ' ', without_link)
    without_spchars = re.sub(r'([^a-zA-Z0-9 ]+)', ' ', without_html)
    tokens = word_tokenize(without_spchars)
    cleaned = [w for w in tokens if not w in stop_words]
    
    lemmatized = [lm.lemmatize(word) for word in cleaned]
    res = tb.detokenize(lemmatized)
    return res


@app.route("/api/sentiment", methods=["POST"])
def handler():
    data = anal.polarity_scores(cleaner(request.json['sentence']))
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=8000)