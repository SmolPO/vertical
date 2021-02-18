from PIL import Image
import pytesseract
import os
from datetime import datetime
import cv2


folder = "D:\scan_folder"


def check_file():
    files = os.listdir(folder)
    for file in files:
        text = str(((pytesseract.image_to_string(Image.open(file), lang='rus'))))
        if "Температура" in text:
            os.replace(file, "D:/after_OCR/covid" + "covid_" + str(datetime.now().date()))
        elif "выдать" in text:
            os.replace(file, "D:/after_OCR/pass" + "выдача_" + str(datetime.now().date()))
        elif "разблокировать" in text:
            os.replace(file, "D:/after_OCR/pass" + "раблокировка_" + str(datetime.now().date()))
        elif "продлить " in text:
            os.replace(file, "D:/after_OCR/pass" + "продление_" + str(datetime.now().date()))
        elif "выходные" or "выходной" in text:
            os.replace(file, "D:/after_OCR/pass" + "выходные_" + str(datetime.now().date()))
        elif "чек" in text:
            date, price, number = next_bill(text, file)

            pass


def next_bill(text, file):
    ind_price = text.rindex("ИТОГ")
    ind_number = text.rindex("ЧЕК")
    year = datetime.now().year
    ind_date = text.rindex(str(year))
    date = text[ind_date-6:ind_date]
    price = text[ind_price+3:ind_price+13]
    number = text[ind_number+5:ind_number+15]
    return date, price, number
