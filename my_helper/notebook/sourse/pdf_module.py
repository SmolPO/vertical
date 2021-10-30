from PIL import Image
import pytesseract
import os
from datetime import datetime as dt
import cv2
import img2pdf


folder = "B:\my_helper\scan"
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

"""
Продление 
Разблокировка
Работа в вых
Выдать
чек
Ковид
накладная
"""


def check_file():
    files = os.listdir(folder)
    count_files = len(files)
    for file in files:
        text = str(((pytesseract.image_to_string(Image.open("B:\my_helper\scan\scan_1.jpg"), lang='rus'))))
        print(text)
        #  os.replace(file, conf.path_OCR + "/covid/" + "covid_" + str(dt.now().date()))
        # go_img2pdf(folder + "/" + file, folder, "covid")
        if "Температура" in text:
            if count_files == 1:
                """Это утренний ковид журнал. 
                Переместить в папку Ковид, преобразовать в PDF и отправить по почте. Адрес записан в настройках."""
                pass
        elif "выдать" in text:
            os.replace(file, conf.path + conf.path_OCR + "/выдача_" + str(dt.now().date()))
        elif "разблокировать" in text:
            os.replace(file, conf.path + conf.path_OCR + "/my_pass" + "/раблокировка_" + str(dt.now().date()))
        elif "продлить " in text:
            os.replace(file, conf.path + conf.path_OCR + "/my_pass" + "/продление_" + str(dt.now().date()))
        elif "ИТОГ" in text:
            date = next_bill(text, "B:\my_helper\scan\scan.jpg")
            return date
        elif "выходные" or "выходной" in text:
            os.replace(file, conf.path + conf.path_OCR + "/my_pass" + "/выходные_" + str(dt.now().date()))


def create_covid():
    pdfs = conf.path_OCR + "/covid"
    files = os.listdir(pdfs)
   # merger = PdfFileMerger()
   # for pdf in files:
    #    merger.append(pdf)
  #  merger.write(pdfs + "/covid_{0}_{1}.pdf".format(dt.now().day, dt.now().month))
    pass


def next_bill(text, file):
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    data, bbox, tmp = detector.detectAndDecode(img)
    return data


def go_img2pdf(file, to_folder, new_name):
    a4_page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
    layout_function = img2pdf.get_layout_fun(a4_page_size)
    pdf = img2pdf.convert(file, layout_fun=layout_function)
    with open(to_folder + "/" + new_name, 'wb') as f:
        f.write(pdf)

