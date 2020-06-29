import pandas as pd
import numpy as np 
from collections import OrderedDict
from spacy.matcher import PhraseMatcher
import spacy
import en_core_web_sm
from ocr_setup import parse


ks = pd.read_excel('food.xlsx')

# ks.head(10)
mst_common = []
shrt = ks['Long_Desc'].tolist()

for item in shrt : 
    item = item.split(',')
    mst_common.append(item[0].lower())
    

mst_common = set(mst_common)
print("Unique enteries present in the data :" ,len(mst_common))


lst = parse()
str_lst = " ".join(lst)

nlp = spacy.load('en')

matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
patterns = [nlp(text) for text in mst_common]
matcher.add("TerminologyList", None, *patterns)
text_doc = nlp(str_lst)
matches = matcher(text_doc)


for i in range(len(matches)):
    match_id, start, end = matches[0]
    print(nlp.vocab.strings[match_id], text_doc[start:end])