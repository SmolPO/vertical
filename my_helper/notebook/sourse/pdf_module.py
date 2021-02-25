from PIL import Image
import pytesseract
import os
from datetime import datetime as dt
from PyPDF2 import PdfFileMerger
import config as conf
import cv2


folder = "D:\scan_folder"


def check_file():
    files = os.listdir(folder)
    for file in files:
        text = str(((pytesseract.image_to_string(Image.open(file), lang='rus'))))
        if "Температура" in text:
            os.replace(file, conf.path + conf.path_OCR + "/covid/" + "covid_" + str(dt.now().date()))
        elif "выдать" in text:
            os.replace(file, conf.path + conf.path_OCR + "/выдача_" + str(dt.now().date()))
        elif "разблокировать" in text:
            os.replace(file, conf.path + conf.path_OCR + "/pass" + "/раблокировка_" + str(dt.now().date()))
        elif "продлить " in text:
            os.replace(file, conf.path + conf.path_OCR + "/pass" + "/продление_" + str(dt.now().date()))
        elif "выходные" or "выходной" in text:
            os.replace(file, conf.path + conf.path_OCR + "/pass" + "/выходные_" + str(dt.now().date()))
        elif "чек" in text:
            date, price, number = next_bill(text, file)
            return date, price, number


def create_covid():
    pdfs = conf.path_OCR + "/covid"
    files = os.listdir(pdfs)
    merger = PdfFileMerger()
    for pdf in files:
        merger.append(pdf)
    merger.write(pdfs + "/covid_{0}_{1}.pdf".format(dt.now().day, dt.now().month))
    pass


def next_bill(text, file):
    ind_price = text.rindex("ИТОГ")
    ind_number = text.rindex("ЧЕК")
    year = dt.now().year
    ind_date = text.rindex(str(year))
    date = text[ind_date-6:ind_date]
    price = text[ind_price+3:ind_price+13]
    number = text[ind_number+5:ind_number+15]
    return date, price, number
