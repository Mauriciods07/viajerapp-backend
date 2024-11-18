from tensorflow.keras.preprocessing.text import Tokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import re

def get_tokenizer(texts):
    nltk.download('stopwords')

    tokenizer = Tokenizer()
    stop_words = stopwords.words('spanish')
    
    X = []
    for sen in texts:
        sentence = sen
        
        for stopword in stop_words:
            sentence = sentence.replace(" " + stopword + " ", " ")
        sentence = sentence.replace("á", "a")
        sentence = sentence.replace("é", "e")
        sentence = sentence.replace("í", "i")
        sentence = sentence.replace("ó", "o")
        sentence = sentence.replace("ú", "u")
                
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = sentence.lower()
        regex_tokenizer = RegexpTokenizer(r'\w+')
        result = regex_tokenizer.tokenize(sentence)
        X.append(TreebankWordDetokenizer().detokenize(result))

    tokenizer.fit_on_texts(X)
    return tokenizer