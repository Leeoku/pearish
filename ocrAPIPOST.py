import requests


def ocr_space_file(filename, overlay=False, api_key='7528f1b76188957', language='eng', istable=True):
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

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'istable': istable,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='7528f1b76188957', language='eng', istable=True):
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

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'istable': istable,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


print(ocr_space_file('receipt2.jpg'))
print(ocr_space_url('https://ocr.space/Content/Images/receipt-ocr-original.jpg'))
