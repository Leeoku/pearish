import pandas as pd, numpy as np
from collections import OrderedDict
import spacy
from spacy.matcher import PhraseMatcher
from ocr_setup import parse
from textblob import TextBlob
from datetime import date
from datetime import timedelta  
import json

# Query the excel sheet and obtain the target food groups. Note not all food group codes used
def food_database():
    df = pd.read_excel("food.xlsx", usecols="B:C")
    food_group_map = {
        100: "dairy",
        1800: "grain",
        2000: "grain",
        500: "meat",
        700: "meat",
        1000: "meat",
        1300: "meat",
        1500: "meat",
        1700: "meat",
        900: "fruit_veg",
        1100: "fruit_veg",
        1600: "fruit_veg",
    }
    df["Food Group"] = df["FdGrp_Cd"].map(food_group_map)
    df_split = df["Long_Desc"].str.split(",", n=1, expand=True)
    df_split.columns = ["Food Name", "Food Name Detail"]
    df = pd.concat([df, df_split], axis=1)
    df = df.groupby("Food Group")["Food Name"].unique()
    dairy = df["dairy"]
    grain = df["grain"]
    meat = df["meat"]
    fruit_veg = df["fruit_veg"]
    food_groups = np.concatenate((dairy, meat, grain, fruit_veg))
    return food_groups

# filter for parsed words, removes stopwords, punctuation and returns
# a tuple of singular and plural words
def filter_words(nlp,all_words):
    text_doc = nlp(all_words)
    
    # removing stop words or punctuation 
    text_doc2 = [] 
    for token in text_doc : 
        if(not token.is_stop and len(token.text) > 2 and not token.text.isnumeric()): 
            # print("token length == ",len(token), " token text len ==", len(token.text), " token text -", token.text)
            text_doc2.append(token.lemma_)
  
    words_string = ' '.join(text_doc2)
    text_blob_object = TextBlob(words_string)
    singular_string = ' '.join(text_blob_object.words.singularize())
    
    # plural_string = ' '.join(text_blob_object.words.pluralize())
    return(singular_string,words_string)
    

# Use the nlp from spacy module  and the PhraseMatcher 
# to match input(parsed reciept words) with the items 
# present in our output code
# returns the items present in the reciept as well as the 
# count of each item in dict() format
def pattern_match():
    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab, attr = 'LOWER') 
    parsed_words = parse()
        
    words_string = ' '.join(parsed_words)
    (single,plural) = filter_words(nlp,words_string)

    text_doc_singular = nlp(single)
    text_doc_plural   = nlp(plural)
    food_groups = food_database()

    # Building the intial list of keywords we want to match the parsed items aganist
    patterns = [nlp(text) for text in food_groups]
    matcher.add("Food Matcher", None, *patterns)
    return(text_doc_singular, text_doc_plural, matcher )

def get_dates() :
    today = date.today()
    present_date = today.strftime("%m/%d/%y")
    today = today + timedelta(days=14)
    expiry_date = today.strftime("%m/%d/%y")

    return(present_date, expiry_date)


def get_results(text_doc_singular, text_doc_plural, matcher):
    matches = matcher(text_doc_singular)
    results = []

    # Matching singulars
    for i in range(len(matches)):    
        match_id, start, end = matches [0]
        # results.append((nlp.vocab.strings[match_id], text_doc_singular[start:end]))
        results.append(text_doc_singular[start:end])

    # Matching plurals
    matches = matcher(text_doc_plural)
    for i in range(len(matches)):    
        match_id, start, end = matches [0]
        # results.append((nlp.vocab.strings[match_id],text_doc_plural[start:end]))
        results.append(text_doc_plural[start:end])

    #Create results with standard template for object
    results = {i: results.count(i) for i in results}
    results_with_dates = []
    today,expiry = get_dates()
    for k, v in results.items():   
        # ind_item = (json.dumps({"name" : str(k), "category" : "placeholder", "purchase_date" : today, "expiration_date" : expiry, 
        #     "count" : v }))
        ind_item = {"name" : str(k), "category" : "placeholder", "purchase_date" : today, "expiration_date" : expiry, 
        "count" : v }
        results_with_dates.append(ind_item)
    return results_with_dates

    results = dict((i, results.count(i)) for i in results)
    return results

if __name__ == "__main__":
    (single,plural,matcher) = pattern_match()
    results = get_results(single,plural,matcher)
    print(results)



