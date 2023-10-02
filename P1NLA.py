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
import spacy

# Tokenization Regular Expression
mytokenizer=RegexpTokenizer(r'\S[A-Z|\.]+ \w*|\'s|[A-Z|a-z]+\'[a-r|t-z]+|\$|[0-9]+\,[0-9]+\,*[0-9|\,]*|[0-9]+\.[0-9]+|\w+|\d+|\S+')

sentence = reuters.raw("training/267")

# Handling the heading in the corpus which are all uppercase words
headingSplit = re.search(r'[A-Z|\s]+\n',sentence)
# Using Regular Expression to just find the the uppercase words to distinguish between heading and body of the text
heading=headingSplit.group().lower()
# Combining the heading and body


body=heading+sentence[heading.find("\n")+1:]
sentence=body

# Using NLTK tokenizer with my custom regex tokenizer
tokenization= mytokenizer.tokenize(sentence)
print("\nSentence =\n",sentence)
print("--------------------------------------------")
print("Tokenization = \n",tokenization)
print("--------------------------------------------")
# Tokenization Examples
examples="Greetings! How have you been on this fine Tuesday? The price of the latest iPhone is $1,200. In scientific notation, 3.5 x 10^7 represents a large number. The meeting is scheduled for 3 PM at 567 Tech Boulevard, Suite 12C, San Francisco, CA. Don't forget to check your email (user@example.com) for important updates."
# print(examples,"\n")
# print(mytokenizer.tokenize(examples))



# SENTENCE SPLITTING
def spaCySentenceSplitting(sentence):
    sentence = sentence.replace('\n','')
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    sentences = [sent.text.strip() for sent in doc.sents]
    print("Sentence Splitting =\n",sentences)
    print("--------------------------------------------")

spaCySentenceSplitting(sentence)
# Example Test case
# value="The quick brown fox jumped over the lazy dog. It happened in the quiet afternoon. Coding is an art. It requires creativity and precision to craft elegant solutions. Have you ever tried skydiving? It's an exhilarating experience that you won't forget. The recipe calls for flour, sugar, and eggs. Mix them well before baking.In the heart of the city, a bustling market comes to life. Vendors shout, and customers haggle for the best deals."
# spaCySentenceSplitting(value)


# POS Tagging
posTag = nltk.pos_tag(tokenization)
print("POS Tagging = \n",posTag)
print("--------------------------------------------")

value1="The copra market of 2020 saw a surge in demand for SpecialtyCopra, a premium variety. Copra-producing nations like Vietnam and Thailand collaborated to address industry challenges. However, climate-induced disruptions in 2022 impacted copra production and market dynamics."


gazetteer = {
    "Country": ["india", "indonesia", "philippines", "malaysia", "vietnam", "thailand", "singapore", "japan", "canada", "australia", "brazil", "united states", "united kingdom", "germany", "france", "italy", "spain", "russia", "china", "south korea", "mexico", "argentina", "south africa", "nigeria", "egypt", "saudi arabia", "turkey", "iran", "australia", "new zealand", "chile", "peru", "colombia", "ecuador", "venezuela", "pakistan", "bangladesh", "sri lanka", "nepal", "afghanistan", "iraq", "syria", "lebanon", "jordan", "israel", "palestine"],
    "Year": ["1987", "1986", "1990", "1995", "2000", "2020", "2022", "2005", "2010", "2015", "2030"],
    "Currency": ["rupiah", "peso", "ringgit", "dong", "baht", "dollar", "euro", "pound", "yen", "rupee", "yuan","$","dls"],
    "Organization": ["U.S. Embassy", "world health organization", "united nations", "red cross", "greenpeace", "UNICEF", "amnesty international", "NASA", "european union", "OPEC"],
    "Unit": ["tonnes", "mln", "mln tonnes", "meters", "liters", "kilograms", "pct", "gallons", "cubic meters", "square kilometers", "grams","kg"],
    "Product": ["copra", "rice", "rubber", "coffee", "sugar", "corn", "wheat", "cotton", "oil", "natural gas", "coal"],
    "Concept": ["margin", "prices", "demand", "supply", "trade", "economy", "market", "sustainability", "innovation", "automation", "blockchain"],
    "Action": ["forecast", "import", "export", "devaluation", "duties", "price", "production", "trade", "investment", "regulation", "merger"],
    "Time": ["am", "pm", "AM", "PM", "3:30", "12:45", "8:00", "10:15", "6:30", "1:00", "9:45"]
}




# Named Entity Recoginiton
ne = nltk.ne_chunk(posTag,binary=True)

# Using ne_chunk to identify Named Entity(NE) but certain NE are not identified by the deafult package in NLTK
# Will use custom method to check with a gazetter list and identify the ones missed by the ne_chunk package

def customNER(ne,gazetteer):
      entities =[]
      if isinstance(ne,nltk.Tree):
            # using nltk tree to find the subtree are get the NE from the posTag value
            for subtree in ne:
                  if isinstance(subtree,nltk.Tree):
                        # if term has the NE tag it is appended to the list
                        if(subtree.label()=="NE"):
                              entities.append(subtree.leaves()[0][0])
                  # else checking if its in the gazetteer list and storing it in the list
                  elif subtree[0].lower() in gazetteer:
                        entities.append(subtree[0])
      return entities

# With this method creating a flat list to store the gazetteer value which will be used in customNER
def listmodification(gazetteer):
      lst=[]
      for key in gazetteer:
            lst.extend(gazetteer[key])
      return lst

finalGaz= listmodification(gazetteer)
NER = customNER(ne, finalGaz)
print("Named Entity Recognition = \n",NER)
print("--------------------------------------------")                  



# Measured Entity Detection
def MeasuredEntityDetection(posTag, gazetteer, ne):
    ouput=[]
      #To focus on expected measured entities, the module first filters away cardinal number terms that are not labeled as named things.
    cd_words=list(filter(lambda x: x[1]=="CD" and x[0] not in ne,posTag))
    nextIndex=dict()
#   Indexing
    for i in cd_words:
          index=0
          if( i in nextIndex.keys()):
                index=posTag.index(i,nextIndex[i]+1)
                nextIndex[i]=index
          else:
                index=posTag.index(i)
                nextIndex[i]=index
          result=""
          if posTag[index][1] == "CD" and all(gaz_word.lower() not in i[0].lower() for gaz_word in gazetteer.get("Year", [])):
            if(posTag[index-1] =="Currency"):
                result+=posTag[index-1][0]
          result+=posTag[index][0]+""
          indexBound=index+4 if len(posTag)>index+4 else len(posTag)
          for j in range(index,indexBound):
                if(posTag[j][1] in ["Unit","Currency","NNS","NN","Product","Time"]) : # add VBP for ( 2 am)
                        result += " " + posTag[j][0]
                  #     result+=" "+posTag[j][0]
          ouput.append(result)
    return ouput

MED = MeasuredEntityDetection(posTag, gazetteer, ne)
print("Measured Entity Detection = \n",MED)

