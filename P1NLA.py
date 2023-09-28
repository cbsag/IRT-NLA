import nltk
# nltk.download("punkt")
from nltk.corpus import reuters
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize,sent_tokenize
import re
from collections import defaultdict
# import sklearn_crfsuite 
# !pip install sklearn-crfsuite
# from sklearn_crfsuite import CRF
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


# Tokenixation
# mytokenizer=RegexpTokenizer(r'[A-Z]+\.[A-Z]+\.|\'s|[0-9]+\,[0-9]+|[0-9]+\.[0-9]+|\w+|\d+|\S') ======= like Embassy's

mytokenizer=RegexpTokenizer(r'[A-Z]+\.[A-Z]+\. \w*|\'s|\$|[0-9]+\,[0-9]+|[0-9]+\.[0-9]+|\w+|\d+|\S+')
sentence = reuters.raw("training/9940")
# sentence="UNITED STATES TO IMPORT BRAZILIAN COFFEE\n The United States is set to import coffee from Brazil in 2022, despite challenges in the coffee market. According to a report by the Brazilian Coffee Association, the U.S. is expected to import over 500,000 bags of Brazilian coffee next year. This move comes as the price of coffee beans worldwide continues to rise, making it a strategic decision for the United States to secure a steady supply of coffee beans.Brazil's coffee production is forecasted to reach 3.5 million tonnes in 2022, marking a significant increase from the previous year. This surge in production is seen as a response to growing global demand for high-quality coffee. It is expected that the Brazilian government will implement measures to support coffee farmers and maintain the country's position as a major coffee exporter."

headindSplit = re.search(r'[A-Z|\s]+\n',sentence)
heading=headindSplit.group().lower()

body=heading+sentence[heading.find("\n")+1:]+".I have one dog. Three handsome pooches. A group of three delightful dogs. Three appealing furry friends."
sentence=body
tokenization= mytokenizer.tokenize(sentence)
print(tokenization)


# SENTENCE SPLITTING
sentenceSplit = nltk.sent_tokenize(sentence)
# print(sentenceSplit)

# POS Tagging
posTag = nltk.pos_tag(tokenization)
print(posTag,"\n","------------------------------------------------------------------------")


# gazetter
gazetteer = {
    "Country": ["Indonesia", "Philippines", "indonesia","phillipines"],
    "Year": ["1987", "1986"],
    "Currency" :["rupiah"],
    "Organization": ["U.S. Embassy"],
    "Unit": ["tonnes", "mln tonnes", "mln","pct"],
    "Product": ["copra"],
    "Concept": ["margin", "prices"],
    "Action": ["forecast", "import", "devaluation", "duties", "price", "production"]
}

# Named Entity Recoginiton

# print(nltk.ne_chunk(posTag,binary=False))


def custom_ner(posTag, gazetteer):
    entities = []
    for token, pos_tag in posTag:
        for category, values in gazetteer.items():
            if token.upper() in [value.upper() for value in values]:
                entities.append((token, category))

    # limitations of this module is that only matched value is stored like posTagged value in Gaz list
    for word,categories in posTag:
                for key, values in gazetteer.items():
                      if word in values:
                            index= posTag.index((word,categories))
                            posTag[index]=(word,key)
    return entities,posTag

# Perform custom NER
recognized_entities= custom_ner(posTag, gazetteer)
print("\n",recognized_entities,"----------")

print("\n",nltk.ne_chunk(posTag,binary=True))

def MeasuredEntityDetection(posTag, gazetteer):
    # unit_patterns = [r"(\d+(\.\d+)?)\s*"]
    ouput=[]
    cd_words=list(filter(lambda x: x[1]=="CD",posTag))
    nextIndex=dict()
    for i in cd_words:
          index=0
          if( i in nextIndex.keys()):
                index=posTag.index(i,nextIndex[i]+1)
                nextIndex[i]=index
          else:
                index=posTag.index(i)
                nextIndex[i]=index
          result=""
          if(posTag[index-1] =="currency"):
                result+=posTag[index-1][0]
          result+=posTag[index][0]+" "
          indexBound=index+4 if len(posTag)>index+4 else len(posTag)
          for j in range(index,indexBound):
                if(posTag[j][1] in ["Unit","Currency","NNS","NN"] ):
                      result+=" "+posTag[j][0]
          ouput.append(result)
    return ouput
print(MeasuredEntityDetection(posTag,gazetteer))

