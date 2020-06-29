import pandas as pd, numpy as np
from collections import OrderedDict
import spacy
from spacy.matcher import PhraseMatcher
from ocr_setup import parse


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
    print(df)
    return dairy, grain, meat, fruit_veg

def nlp():
    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab, attr = 'LOWER')
    parsed_words = parse()
    words_string = ' '.join(parsed_words)
    food_groups = food_database()
    fruit_veg_string = food_groups[3]
    #fruit_veg_string = np.array2string(food_groups[3])
    patterns = [nlp(text) for text in fruit_veg_string]
    matcher.add("TerminologyList", None, *patterns)
    text_doc = nlp(words_string)
    matches = matcher(text_doc)
    #for receipt_match in matches:
        # match_id, start, end = receipt_match [0]
        # print(nlp.vocab.strings[match_id], text_doc[start:end])
    for i in range(len(matches)):    
        match_id, start, end = matches [0]
        print(nlp.vocab.strings[match_id], text_doc[start:end])

    #Avi's Code

# ks = pd.read_excel('food.xlsx')

# # ks.head(10)
# mst_common = []
# shrt = ks['Long_Desc'].tolist()

# for item in shrt : 
#     item = item.split(',')
#     mst_common.append(item[0].lower())
    

# mst_common = set(mst_common)
# print("Unique enteries present in the data :" ,len(mst_common))


# lst = parse()
# str_lst = " ".join(lst)

# nlp = spacy.load('en')

# matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
# patterns = [nlp(text) for text in mst_common]
# matcher.add("TerminologyList", None, *patterns)
# text_doc = nlp(str_lst)
# matches = matcher(text_doc)


# for i in range(len(matches)):
#     match_id, start, end = matches[0]
#     print(nlp.vocab.strings[match_id], text_doc[start:end])


    #dairy_string = np.array2string(food_groups[0])
    #meat_string = np.array2string(food_groups[3])
    #food_groups_strings = np.array2string(food_groups)
    # patterns = [nlp(text) for text in meat_string]
    # matcher.add("TerminologyList", None, *patterns)
    # text_doc = nlp(words_string)
    # matches = matcher(text_doc)
    # match_id, start, end = matches [1]
    # print(nlp.vocab.strings[match_id], text_doc[start:end])

    # words_string = ''.join(parsed_words)
    # doc = nlp(words_string)
    # matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

def search():
    food_groups = food_database()[0]
    #print(food_groups)
    #print(len(food_groups))

    # print(df['dairy'])
    # common_words = []
    # description = df['Long_Desc'].tolist()
    # for item in description:
    #     item = item.split(',')
    #     common_words.append(item[0].lower())
    # m = np.asarray(common_words)
    # set_word = set(common_words)

    #d = dict(zip(df.index, df.values))
#     #list version
#     #parsed_database = list(OrderedDict.fromkeys(common_words))

# print(data.get('ParsedResults')[0]['TextOverlay']['Lines'][22].get('LineText'))
# print(i.get('LineText'))
# print((new_data["ParsedResults"][0].values()))
# filtered_data = (new_data["ParsedResults"][0].get('LineText'))

if __name__ == "__main__":
    food_database()
    #search()
    nlp()
    #parse()
