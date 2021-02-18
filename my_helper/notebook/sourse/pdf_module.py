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
            next_bill(text, file)
            pass


def next_bill(text, file):
    ind_price = text.rindex("Итог")
    ind_number = text.rindex("ЧЕК")
    ind_date = text.rindex("")
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
filename = "D:\my_img.jpg"
text = str(((pytesseract.image_to_string(Image.open(filename), lang='rus'))))
text = text.replace('-\n', '')
print(text)
j = input()
