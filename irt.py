import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



# this clean_text function is used because I encontered (special character)
def clean_text(text):
    cleaned_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)
    cleaned_text = ' '.join(cleaned_text.split())  
    return cleaned_text

def remove_custom_stopwords(filePath, endDir, custom_stopwords=None):
    if custom_stopwords is None:
        custom_stopwords = []

    for filePath in filePath:
        with open(filePath, 'r', encoding='utf-8') as file:
            text = file.read()
        # print("Before",len(text))
        words = text.split()

        filtered_words = [word for word in words if word.lower() not in custom_stopwords]

        filtered_text = ' '.join(filtered_words)

        output_filename = os.path.splitext(os.path.basename(filePath))[0] + '_filtered.txt'
        output_file_path = os.path.join(endDir, output_filename)
        # print("After",len(filtered_text),"\n")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(filtered_text)


# PORTER STEMMING ALGORITHM
def porterStemming(filePaths,endDir):
    stemmer = PorterStemmer()
    for filePath in filePaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            text = file.read()

        words = text.split()

        stemmed_words = [stemmer.stem(word) for word in words]

        stemmed_text = ' '.join(stemmed_words)

        output_filename = os.path.splitext(os.path.basename(filePath))[0] + '_stemmed.txt'
        output_file_path = os.path.join(endDir, output_filename)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(stemmed_text)



def tokenizzzToLowerCase(filePath,endDir):
    for i in filePath:
        with open(i, 'r', encoding='utf-8') as file:
            text= file.read()
        
        text = text.lower()

        outputFilename = os.path.splitext(os.path.basename(i))[0] + '_to.txt'
        outputFilePath = os.path.join(endDir, outputFilename)

        with open(outputFilePath,'w',encoding='utf-8') as output_file:
            output_file.write(text)

# Second method in pipeline
# def tokenizzz(filePath, endDir):
#     tokens_list = []

#     for i, file_path in enumerate(filePath):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             text = file.read()
#             # Tokenization and lowercasing
#             tokens = word_tokenize(text.lower())  # Lowercase tokens
#             tokens_list.append(tokens)

#             outputFilename = os.path.splitext(os.path.basename(file_path))[0] + '_tokens.txt'
#             outputFilePath = os.path.join(endDir, outputFilename)

#             with open(outputFilePath, 'w', encoding='utf-8') as output_file:
#                 for token in tokens:
#                     output_file.write(token + '\n')

#     return tokens_list




def tokenizzz(filePath,endDir):
    tokens_list = []  #

    for i, file_path in enumerate(filePath):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = word_tokenize(text)  
            tokens_list.append(tokens)  

            outputFilename = os.path.splitext(os.path.basename(file_path))[0] + '_tokens.txt'
            outputFilePath = os.path.join(endDir, outputFilename)

        
        with open(outputFilePath, 'w', encoding='utf-8') as output_file:
            for token in tokens:
                output_file.write(token + '\n')
    # this method returns a 
    return tokens_list



def read_reuters_corpus(corpus_root,endDir):
    documents = []
    # metadata = []
    articles=[]
    articelCounter =0
    num_articles=0
    for root, _, files in os.walk(corpus_root):
        for filename in os.listdir(root):
            if articelCounter<=num_articles:
                break
        
        # for filename in os.listdir(root):
            if filename.endswith(".sgm"): 
                with open(os.path.join(root, filename), 'r', encoding='ISO-8859-1') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    for newsitem in soup.find_all('reuters'):
                        body = newsitem.find('text')
                        if body:
                            artText = body.get_text()
                            cleaned_article_text = clean_text(artText)
                            articles.append(cleaned_article_text)
                            # documents.append(body.get_text())
                            articelCounter+=1
                            if articelCounter >= num_articles:
                                break
    # print(art)
    # this list is used to store the newly created files name so I can traverse this file and access the values to be sent to the other methods in the pipeline
    filePath=[]
    for i,artText in enumerate(articles):
       output_filename = os.path.join(endDir, f'article_{i+1}.txt')
       with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(artText) 
            
       filePath.append(output_filename)       
    # return documents
    return filePath

    


filePath=read_reuters_corpus(r'C:/Users/cbsag/Desktop/NLA/IRT','C:/Users/cbsag/Desktop/NLA/Output')
tokenizzz(filePath,'C:/Users/cbsag/Desktop/NLA/Tokenized value')
tokenizzzToLowerCase(filePath,'C:/Users/cbsag/Desktop/NLA/LowerCase')
porterStemming(filePath,'C:/Users/cbsag/Desktop/NLA/Stemmed')
custom_stopwords= [
    'a', 'an', 'and', 'are', 'as', 'at', 'for', 'from', 'has', 'he', 'in', 'is',
    'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'with'
]

custom_stopwords.append(stopwords.words('english'))

remove_custom_stopwords(filePath,'C:/Users/cbsag/Desktop/NLA/stopwords', custom_stopwords)
# nltk.download('stopwords')
# print(custom_stopwords.append(stopwords.words('english')))

