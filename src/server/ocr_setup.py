from api import ocr_key
import requests, json
from collections import OrderedDict
import os, glob
from pathlib import Path

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
    #return r.content.decode()
    return r.json()
  
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


# API response and obtain "LineText"
def parse():
    cwd = os.getcwd()
    final_directory = os.path.join(cwd, 'img')
    #Checks to see if there is an img folder that isn't empty
    if os.path.isdir(final_directory) != True or len(os.listdir('./img')) == 0 :
        return f"Image folder is empty or doesn't exist"
    #Checks to ensure there is only 1 image max in our existing /img folder
    elif len(os.listdir('./img')) > 1:
        files = sorted(Path(final_directory).iterdir(), key=os.path.getctime, reverse=True)
        for file in files[1:]:
            os.remove(file)
    else:
        #Look for a pic named receipt.extension, need to add logic if greater than allowed pic size
        img_file = os.listdir('./img')[0]
        img_file_path = './img/' + img_file
        data = ocr_space_file(img_file_path)
        # data = ocr_space_url("https://ocr.space/Content/Images/receipt-ocr-original.jpg")
        lines = data.get("ParsedResults")[0]["TextOverlay"]["Lines"]
        words = [line.get("LineText").lower() for line in lines]
        return words
    
if __name__ == "__main__":
    parse()