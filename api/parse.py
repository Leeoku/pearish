import requests, json
import pandas as pd, numpy as np
from api import ocr_key
from collections import OrderedDict


def ocr_space_file(
    filename, overlay=False, api_key=ocr_key, language="eng", istable=True, scale=True
):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7

    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    :param istable: parses output as a table
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
        "istable": istable,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image", files={filename: f}, data=payload,
        )
    return r.content.decode()

g
def ocr_space_url(
    url, overlay=False, api_key=ocr_key, language="eng", isTable=True, scale=True
):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7

    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    :param isTable: parses output as a table
    """

    payload = {
        "url": url,
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
        "isTable": isTable,
    }
    r = requests.post("https://api.ocr.space/parse/image", data=payload,)
    # return r.content.decode()

    # Change this return in source code to return JSON object, not string
    return r.json()


# API response and obtaing "LineText"
def parse():
    data = ocr_space_url("https://ocr.space/Content/Images/receipt-ocr-original.jpg")
    lines = data.get("ParsedResults")[0]["TextOverlay"]["Lines"]
    words = [line.get("LineText").lower() for line in lines]
    # print(words)
    return words


# Query the excel sheet and obtain the target food groups. Note not food group codes used
def FoodDatabase():
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
    
    return dairy, grain, meat, fruit_veg

    # print(df['dairy'])
    # common_words = []
    # description = df['Long_Desc'].tolist()
    # for item in description:
    #     item = item.split(',')
    #     common_words.append(item[0].lower())
    # m = np.asarray(common_words)
    # set_word = set(common_words)


#     #list version
#     #parsed_database = list(OrderedDict.fromkeys(common_words))

# print(data.get('ParsedResults')[0]['TextOverlay']['Lines'][22].get('LineText'))
# print(i.get('LineText'))
# print((new_data["ParsedResults"][0].values()))
# filtered_data = (new_data["ParsedResults"][0].get('LineText'))

if __name__ == "__main__":
    parse()
    FoodDatabase()
