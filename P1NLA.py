import nltk
# nltk.download("punkt")
from nltk.corpus import reuters
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize,sent_tokenize
# nltk.download('averaged_perceptron_tagger')


# Tokenixation
# mytokenizer=RegexpTokenizer(r'[A-Z]+\.[A-Z]+\.|\'s|[0-9]+\,[0-9]+|[0-9]+\.[0-9]+|\w+|\d+|\S') ======= like Embassy's
mytokenizer=RegexpTokenizer(r'[A-Z]+\.[A-Z]+\. \w*|\'s|[0-9]+\,[0-9]+|[0-9]+\.[0-9]+|\w+|\d+|\S')
sentence = reuters.raw("training/267")
print(sentence)
tokenization= mytokenizer.tokenize(sentence)
print(tokenization)

# SENTENCE SPLITTING
sentenceSplit = nltk.sent_tokenize(sentence)
print(sentenceSplit)

# POS Tagging
posTag = nltk.pos_tag(tokenization)
print(posTag)

# gazetter
gazetteer = {
    "Country": ["INDONESIA", "PHILIPPINES"],
    "Year": ["1987", "1986"],
    "Currency" :["rupiah"],
    "Organization": ["U.S. Embassy"],
    "Unit": ["tonnes", "mln tonnes", "mln","pct"], '''Is this correct way/approach'''
    "Product": ["copra"],
    "Concept": ["margin", "prices"],
    "Action": ["forecast", "import", "devaluation", "duties", "price", "production"]
}

# Named Entity Recoginiton



