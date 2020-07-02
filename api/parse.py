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
    # print(type(food_groups))
    #return dairy, grain, meat, fruit_veg
    return food_groups


# Use the nlp module PhraseMatcher to match input(parsed reciept words) with the items 
# present in our output code
def patter_match():

    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab, attr = 'LOWER')

   # parse the reciept words and covert the list to a string 
    parsed_words = parse()
    words_string = ' '.join(parsed_words)
    food_groups = food_database()
    fruit_veg_string = food_groups[3]]

    # Building the intial list of keywords we want to match the parsed items aganist
    patterns = [nlp(text) for text in food_groups]
    matcher.add("TerminologyList", None, *patterns)

    text_doc = nlp(words_string)
    matches = matcher(text_doc)
    
    # printing all th matches, TerminologyList is the name of the our patter matcher
    for i in range(len(matches)):    
        match_id, start, end = matches [0]
        print(nlp.vocab.strings[match_id], text_doc[start:end])
    


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
    nlp = spacy.load('en')
    matcher = PhraseMatcher(nlp.vocab, attr = 'LOWER') 
    parsed_words = parse()
    
    # parsed_words = ['walmart', 'save money. live better.', 
    # '( 330 ) 339 -', '3991', 'manager diana earnest',
    #  '231 bluebell dr sw', 'new philadelphia oh 44663',
    #   '02115 009044 44', '01301', 'pet toy', 'floppy puppy', 
    #   'sssupreme s', 'z . 5 squeak', 'munchy dmbel', 'dog treat', 
    #   'ped pch 1', 'ped pch 1', 'coupon 23100', '1--inymd smores',
    #    'french drsng', '3 oranges', 'baby carrots', 'collards',
    #     'calzone', 'mm rvw mnt', 'stkobrlplabl', 'stkobrlplabl', 
    #     'stko sunflwr', 'stko sunflwr', 'stko sunflwr',
    #     'stko sunflwr', 'bling beads', 'great value', 
    #     'lipton', 'dry dog', 'tax', 'us debit', '004747571658', 
    #     '004747514846', '070060332153', '084699803238', '068113108796',
    #      '007119013654', '002310011802', '002310011802', '052310037000', '088491226837', '004132100655', '001466835001', '003338366602', '1', '000000004614k1', '005208362080 f', '003399105848', '001558679414', '001558679414', '001558679410', '001558679410', '001558679410', '001558679410', '076594060699', '007874203191 f', '001200011224 f', '002310011035', '1', 'subtotal', '6.750', 'total', 'visa tend', '5', '12 .', '9166', '1.97', '1.97', '4.97', '5.92', '3.77', '2.92', '0.50', '0.50', '1.00-0', '3.98', '1.98', '.47', '1.48', '1.24', '2.50', '19.77', '1.97', '1.97', '0.97', '0.97', '0.97', '0.97', '0.97', '9.97', '4.48', '44', '93.62', '4.59', '98.21', '98.21', '1', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'o', 'o', 'o', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'o', 'x', 'x', 'o', 'approval # 572868', 'ref # 720900544961', 'trans id', '387209239650894', 'validation - 87hs', 'payment service', 'aid a0000000980840', 'tc 51319ca81dcz2bc7', 'terminal # sc010764', '*signature ver ified', '07/28/17', '02 : 39 : 48', 'change due', '# items sold 25', '0443 0223 1059 8001 5140', 'low'
    # , 'ices you can trust .', 'every', '0.00', 'day .', '07/28/17', 
    # '02 : 39 : 48']
    
    
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

    results = {i: results.count(i) for i in results}

    results_with_dates = []
    today,expiry = get_dates()
    for k, v in results.items():   
        ind_item = (json.dumps({"name" : str(k), "category" : "placholder", "purchase_date" : today, "expiration_date" : expiry, 
            "count" : v }))

        results_with_dates.append(ind_item)

    return results_with_dates
