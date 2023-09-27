import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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
    tokens = word_tokenize(text)
    return tokens

def process_article(article_text, article_output_folder):
    custom_stopwords = [
        'a', 'an', 'and', 'are', 'as', 'at', 'for', 'from', 'has', 'he', 'in', 'is',
        'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'with'
    ]
    custom_stopwords.extend(stopwords.words('english'))
    # pivot_text=article_text

    # Tokenization
    pivot2_text = tokenizzz(article_text)
    # print(pivot1_text)
    tokens_output_file = os.path.join(article_output_folder, 'Tokenizer-output.txt')
    with open(tokens_output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(" ".join(pivot2_text))

    # Lowercasing
    
    pivot2_text = tokenizzzToLowerCase(pivot2_text)
    # print(pivot2_text)
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

def process_reuters_corpus(corpus_root, output_root, num_articles=5):
    article_count = 0  # Counter for processed articles
    for root, _, files in os.walk(corpus_root):
        for filename in files:
            if article_count >= num_articles:
                break
            if filename.endswith(".sgm"):
                with open(os.path.join(root, filename), 'r', encoding='ISO-8859-1') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    for i, newsitem in enumerate(soup.find_all('reuters')):
                        if article_count >= num_articles:
                            break
                        body = newsitem.find('text')
                        if body:
                            artText = body.get_text()
                            cleaned_article_text = clean_text(artText)
                            article_output_folder = os.path.join(output_root, f'Article_{i + 1}')
                            os.makedirs(article_output_folder, exist_ok=True)
                            process_article(cleaned_article_text, article_output_folder)
                            article_count += 1

# Usage to process only the first five articles
corpus_root = 'C:/Users/cbsag/Desktop/NLA/IRT'
output_root = 'C:/Users/cbsag/Desktop/NLA/Output'
num_articles_to_process = 5
process_reuters_corpus(corpus_root, output_root, num_articles_to_process)

