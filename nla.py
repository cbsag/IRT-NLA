from nltk.corpus import reuters
from nltk.tokenize import word_tokenize

# nltk.download('reuters')

categories = reuters.categories()
# t9920WordLen = categories.words('training/9920')
fields = len(reuters.fileids())
words = reuters.words('training/9920')
sentence = len(reuters.sents('training/9920'))
# print("Sentence",sentence)

single_word_prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding', 'round', 'since', 'through', 'to', 'toward', 'under', 'underneath', 'until', 'unto', 'up', 'upon', 'with', 'within', 'without']


count = sum (1 for word in words if word.lower() in single_word_prepositions)

reuters_index={}

for category in categories:
    fieldId = reuters.fileids(category)
    reuters_index[category] = fieldId

def word_freq(word, file_id):
    tokens = word_tokenize(reuters.raw(file_id))
    word_count = tokens.count(word)

    return word_count

for category, fieldId in reuters_index.items():
    # print(f"Category: {category}, FieldID: {fieldId}")
    frequency = word_freq(category, fieldId)
    print(f"The word '{category}' appears {frequency}'.")  
    



# def word_freq(word, file_id):
#     # Tokenize the text of the specified file
#     tokens = word_tokenize(reuters.raw(file_id))

#     # Count the frequency of the word
#     word_count = tokens.count(word)

#     return word_count



