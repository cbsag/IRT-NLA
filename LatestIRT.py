import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


# this clean_text function is used because I encontered (special character)
def clean_text(text):
    cleaned_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text

def remove_custom_stopwords(text, custom_stopwords=None):
    if custom_stopwords is None:
        custom_stopwords = []

    words = text.split()
    filtered_words = [word for word in words if word.lower() not in custom_stopwords]
    filtered_text = ' '.join(filtered_words)
    return filtered_text

def porterStemming(text):
    stemmer = PorterStemmer()
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text

def tokenizzzToLowerCase(text):
    lowercased_tokens = []

    # Iterate through the tokens in the list and make each token lowercase
    for token in text:
        lowercased_token = token.lower()
        lowercased_tokens.append(lowercased_token)

    # Join the lowercase tokens into a single string
    lowercased_text = ' '.join(lowercased_tokens)
    # lowercased_text = text.lower()
    
    return lowercased_text

def tokenizzz(text):
    mytokenizer=RegexpTokenizer(r'\S[A-Z|\.]+ \w*|\'s|[A-Z|a-z]+\'[a-r|t-z]+|\$|[0-9]+\,[0-9]+\,*[0-9|\,]*|[0-9]+\.[0-9]+|\w+|\d+|\S+')

    tokens = mytokenizer.tokenize(text)
    return tokens

def process_article(article_text, article_output_folder):
    # Custom Stopwords list - as per the project requirement
    custom_stopwords = [
        'a', 'an', 'and', 'are', 'as', 'at', 'for', 'from', 'has', 'he', 'in', 'is',
        'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'with'
    ]
    # Extending to the NLTK's stopwords
    custom_stopwords.extend(stopwords.words('english'))
    
    # Tokenization
    pivot2_text = tokenizzz(article_text)
    tokens_output_file = os.path.join(article_output_folder, 'Tokenizer-output.txt')
    with open(tokens_output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(" ".join(pivot2_text))

    # Lowercasing
    pivot2_text = tokenizzzToLowerCase(pivot2_text)
    lowercased_output_file = os.path.join(article_output_folder, 'Lowercased-output.txt')
    with open(lowercased_output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(pivot2_text)

    # Stemming
    pivot2_text = porterStemming(pivot2_text)
    stemmed_output_file = os.path.join(article_output_folder, 'Stemmed-output.txt')
    with open(stemmed_output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(pivot2_text)

    # Stopword Removal
    pivot2_text = remove_custom_stopwords(pivot2_text, custom_stopwords)
    no_stopword_output_file = os.path.join(article_output_folder, 'No-stopword-output.txt')
    with open(no_stopword_output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(pivot2_text)

    # Write stopwords used
    stopwords_used_file = os.path.join(article_output_folder, 'Stopwords-used-for-output.txt')
    with open(stopwords_used_file, 'w', encoding='utf-8') as output_file:
        output_file.write("\n".join(custom_stopwords))

# This function is used to read the corpus file from the local storage and traverse 
# to the sgm files and select first five Reuter’s news items in the corpus 
def process_reuters_corpus(corpus_root, output_root, num_articles=5):
    article_count = 0  # Counter for processed articles
    for root, _, files in os.walk(corpus_root):
        for filename in files:
            if article_count >= num_articles:
                break
            # traversing to the .sgm file path
            if filename.endswith(".sgm"):
                with open(os.path.join(root, filename), 'r', encoding='ISO-8859-1') as file:
                    # using beautifulSoup to parse the retures file
                    soup = BeautifulSoup(file, 'html.parser')
                    for i, newsitem in enumerate(soup.find_all('reuters')):
                        # this counter is used to select the first five files
                        if article_count >= num_articles:
                            break
                        # accesing the text part of the file
                        body = newsitem.find('text')
                        if body:
                            artText = body.get_text()
                            cleaned_article_text = clean_text(artText)
                            article_output_folder = os.path.join(output_root, f'Article_{i + 1}')
                            # making the folders for the five news article and calling the functions to
                            os.makedirs(article_output_folder, exist_ok=True)
                            process_article(cleaned_article_text, article_output_folder)
                            article_count += 1

# Usage to process only the first five articles
# To run the code change the below directories alone
corpus_root = 'C:/Users/cbsag/Desktop/NLA/IRT'
output_root = 'C:/Users/cbsag/Desktop/NLA/Output'
num_articles_to_process = 5
process_reuters_corpus(corpus_root, output_root, num_articles_to_process)

