import requests, json
import pandas as pd
from api import ocr_key


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

#API response and obtaing "LineText"
def parse():
    data = ocr_space_url("https://ocr.space/Content/Images/receipt-ocr-original.jpg")
    lines = data.get("ParsedResults")[0]["TextOverlay"]["Lines"]
    words = [line.get("LineText") for line in lines]
    return words

#Query the excel sheet and obtain the target food groups. Note not food group codes used
def FoodDatabase():
    df = pd.read_excel("food.xlsx", usecols="B:C")
    food_group_code = df['FdGrp_Cd']
    dairy = df[food_group_code.isin(['100'])]['Long_Desc'].tolist()
    grain = df[food_group_code.isin(['1800', '2000'])]['Long_Desc'].tolist()
    meat = df[food_group_code.isin(['500', '700', '1000', '1300', '1500', '1700'])]['Long_Desc'].tolist()
    fruit_veg = df[food_group_code.isin(['900', '1100','1600'])]['Long_Desc'].tolist()
    return dairy, grain, meat, fruit_veg

# print(food_data)        
# print(data.get('ParsedResults')[0]['TextOverlay']['Lines'][22].get('LineText'))
# print(i.get('LineText'))
# print((new_data["ParsedResults"][0].values()))
# filtered_data = (new_data["ParsedResults"][0].get('LineText'))
# data['Words'] = [json.loads(s) for s in data['Words']]

if __name__ == "__main__":
    parse()
    FoodDatabase()
