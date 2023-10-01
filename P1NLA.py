from nltk.corpus import reuters
from nltk.tokenize import RegexpTokenizer
import nltk
import re
input=reuters.raw("training/267")

#TOKENIZATION
#split heading
split_heading=re.search(r"[A-Z|\s]+\n",input)
heading=split_heading.group().lower()
body=heading+input[heading.find("\n")+1:]


print(body)

tokenizer=RegexpTokenizer(r'\S[A-Z|\.]+ \w*|\'s|[A-Z|a-z]+\'[a-r|t-z]+|\$|[0-9]+\,[0-9]+\,*[0-9|\,]*|[0-9]+\.[0-9]+|\w+|\d+|\S+')

tokenized_input=tokenizer.tokenize(body)
print(tokenized_input)
split_sents=nltk.sent_tokenize(body)
print(split_sents)


#POS Tagging
# from nltk.tag import StanfordPOSTagger
# model='/Users/hari/Downloads/stanford-postagger-full-2020-11-17/models/english-bidirectional-distsim.tagger'
# jar='/Users/hari/Downloads/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
# st = StanfordPOSTagger(model,jar,encoding="utf8")

tagged_input=nltk.pos_tag(tokenized_input,lang="eng")
print(tagged_input)
# st = StanfordPOSTagger(model,jar,encoding="utf8")
# print(st.tag(tokenized_heading))

#gazetter
gazetteer={"COUNTRY":["indonesia","philippines","united states of america","australia","india","singapore","china","russia","germany","thailand","japan"],
          "currency":["rupiah","$","dlr","dlrs"],
          "units":["pct","mln","tonnes","billion","kg","m/s","kms","km/h"],
          "Organization":["u.s. embassy","n.a.s.a"],
          "date":["1987","1986"],
          "product":["copra","rice","wheat",""],
          "time":["am","pm","AM","PM","hrs","min","secs","sec","hours","minutes","seconds","hour","minute","second","hr","min"]
          }

# for Key in gazetter:
#     for values in gazetter[key]:
#         try:
#             index=tokenized_input.index(values)
#             if(index>=0):
#                 tagged_input[index]=(values,key)
#                 print(tagged_input[index])
#         except:
#             continue


          
#Named Entity Recognition


    # for word,categories in tagged_input:
    #     for key,value in gazetter.items():
    #         if word.lower() in value:
    #             index=tagged_input.index((word,categories))
    #             tagged_input[index]=(word,key)

# def custom_NER(named_entity,gaz_list):
#     entities=[]
#     if isinstance(named_entity,nltk.Tree):
#         val=named_entity.leaves()[0][0]
#         if named_entity.label()=="NE" or val.lower() in gaz_list:
#             entities.append(val)
        
#         else:
#             for subtree in named_entity:
#                 entities.extend(custom_NER(subtree,gaz_list))
#     return entities


def custom_NERI(named_entity,gaz_list):
    entities=[]
    if isinstance(named_entity,nltk.Tree):
       
        for subtree in named_entity:
            if isinstance(subtree,nltk.Tree):
                if(subtree.label()=="NE"):
                    entities.append(subtree.leaves()[0][0])
            elif subtree[0].lower() in gaz_list:
                entities.append(subtree[0])
    return entities


def gazetteer_modulation(gazetteer):
    list=[]
    for key in gazetteer:
        list.extend(gazetteer[key])

    return list

ne=nltk.ne_chunk(tagged_input,binary=True)
print(ne)
consolidated_gazetteer_list=gazetteer_modulation(gazetteer)
named_ent=custom_NERI(ne,consolidated_gazetteer_list)
print(named_ent)



#Measured Entity Recogniton

# def MeasuredEntityModule(tagged_input,gazetteer):
#     output=[]
#     CD_words=list(filter(lambda x: x[1]=="CD" ,tagged_input))
#     nextIndex=dict()
#     for i in CD_words:
#         index=0
#         if(i in nextIndex.keys()):
#             index=tagged_input.index(i,nextIndex[i]+1)
#             nextIndex[i]=index
#         else:
#             index=tagged_input.index(i)
#             nextIndex[i]=index
#         result=""
#         if tagged_input[index-1][1]=="currency":
#             result+=tagged_input[index-1][0]+" "
#         result+=tagged_input[index][0]
#         endIndex=index+4 if len(tagged_input)>index+4 else len(tagged_input)
#         for j in range(index,endIndex):
#             if(tagged_input[j][1] in ["currency","units","NNS","NN","product","time"]):
#                 result+=" "+tagged_input[j][0]
#         output.append(result)
#     return outputà

def MeasuredEntityModule(tagged_input,gazetteer,named_ent):
    output=[]
    CD_words=list(filter(lambda x: x[1]=="CD" and x[0] not in named_ent ,tagged_input))
    nextIndex=dict()
    for i in CD_words:
        index=0
        if(i in nextIndex.keys()):
            index=tagged_input.index(i,nextIndex[i]+1)
            nextIndex[i]=index
        else:
            index=tagged_input.index(i)
            nextIndex[i]=index
        result=""
        if tagged_input[index-1][1]=="currency":
            result+=tagged_input[index-1][0]+" "
        result+=tagged_input[index][0]
        endIndex=index+4 if len(tagged_input)>index+4 else len(tagged_input)
        for j in range(index,endIndex):
            if(tagged_input[j][1] in ["currency","units","NNS","NN","product","time"]):
                result+=" "+tagged_input[j][0]
        output.append(result)
    return output
meList=MeasuredEntityModule(tagged_input,gazetteer,named_ent)
print(meList)
