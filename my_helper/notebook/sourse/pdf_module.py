from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtWidgets import QInputDialog
import PyPDF2
import pytesseract
import os
from datetime import datetime as dt
from my_helper.notebook.sourse.database import get_path, get_path_ui
from my_email import send

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
sub = "Ковидный журнал " + "ООО 'Вертикаль'"
to_email = "kalent_ivan@mail.ru"
body_text = "Доброе утро!"
folder = "B:/my_helper/Сканы"
designer_file_pdf = get_path_ui("pdf_module")
designer_file_email = get_path_ui("email")


class PDFModule(QDialog):
    def __init__(self, parent):
        super(PDFModule, self).__init__()
        self.parent = parent
        if not self.check_start():
            return
        self.b_covid.clicked.connect(self.ev_covid)
        self.b_note.clicked.connect(self.ev_note)
        self.b_other.clicked.connect(self.ev_open)

    def check_start(self):
        self.status_ = True
        self.path_ = designer_file_pdf
        try:
            uic.loadUi(designer_file_pdf, self)
            return True
        except:
            mes.question(self, "Сообщение", "Не удалось открыть форму " + designer_file_pdf, mes.Cancel)
            self.status_ = False
            return False

    def ev_covid(self):
        path_file = self.check_input_c19()
        if not path_file:
            return False
        path_to = get_path("path") + get_path("path_covid") + "/" + str(dt.now().date()) + ".pdf"
        answer = mes.question(self, "Сообщение", "Отправить ковидны журнал на почту " + to_email, mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            os.replace(path_file, path_to)
            send(sub, body_text, to_email, path_to)
        pass

    def check_input_c19(self):
        folder = get_path("path") + get_path("path_scan")
        if len(os.listdir(folder)) > 1:
            file_name = QFileDialog.getOpenFileName(self, "Выбрать файл",
                                                         folder, "PDF Files(*.pdf)")
            return folder + "/" + os.listdir(folder)[0]
        elif not os.listdir(folder):
            mes.question(self, "Сообщение", "Файл не найден. Отсканируйте ковидный журнал в формате PDF", mes.Cancel)
            return False
        else:
            return folder + "/" + os.listdir(folder)[0]

    def check_input_n(self):
        folder = get_path("path") + get_path("path_scan")
        files = os.listdir(folder)
        files.sort()
        if not files:
            mes.question(self, "Сообщение", "Файл не найден. Отсканируйте служебную в формате PDF", mes.Cancel)
            return False
        for file in files:
            if not ".pdf" in file:
                mes.question(self, "Сообщение", "В папке есть не только файлы .pdf. "
                                                "Оставляйте в папке только необходимые файлы", mes.Cancel)
                return False

    def ev_note(self):
        folder = get_path("path") + get_path("path_scan")
        files = os.listdir(folder)
        files.sort()
        if not self.check_input_n():
            return
        text, ok = QInputDialog.getInt(self, 'Сообщение', 'Укажите номер исходящего')
        if not text:
            return
        pdf_merger = PyPDF2.PdfFileMerger()
        path_to = get_path("path") + get_path("path_notes_pdf") + "/" + str(text) + "_" + str(dt.now().date()) + ".pdf"
        for doc in files:
            print(str(folder + "/" + doc))
            if ".pdf" in doc:
                pdf_merger.append(str(folder + "/" + doc))
        pdf_merger.write(path_to)
        wnd = SendPost(self.parent.db, path_to)
        if not wnd.status_:
            mes.question(self, "Сообщение", "Не найден файл дизайна " + wnd._path, mes.Cancel)
            return
        wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
        wnd.exec_()
        for doc in files:
            os.remove(str(folder + "/" + doc))

    def ev_open(self):
        pass


class SendPost(QDialog):
    def __init__(self, db, path):
        super(SendPost, self).__init__()
        if not self.check_start():
            return
        self.db = db
        self.b_ok.clicked.connect(self.ev_send)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.path = path
        self.init_emails()
        self.sub = ""
        self.to_email = ""
        self.body_text = ""

    def check_start(self):
        self.status_ = True
        self.path_ = designer_file_email
        try:
            uic.loadUi(designer_file_email, self)
        except:
            mes.question(self, "Сообщение", "Не удалось открыть форму " + designer_file_email, mes.Cancel)
            self.status_ = False
            return False

    def ev_send(self):
        self.my_sub = self.topic.text()
        self.to_email = self.email.currentText()
        self.body_text = self.note.toPlainText()
        if not self.check_input():
            return False
        answer = mes.question(self, "Сообщение", "Отправить служебную записку на согласование? " + self.to_email,
                              mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            send(self.my_sub, self.body_text, self.to_email, self.path)

    def ev_cancel(self):
        self.close()

    def init_emails(self):
        rows = self.db.get_data("email", "bosses")
        for item in rows:
            print(item)
            self.email.addItem(item[0])

    def check_input(self):
        return True


"""def check_file(parent):
    files = os.listdir(folder)
    files.sort()
    path_covid = "B:/my_helper/Служебки/covid"
    count_files = len(files)
    for file in files:
        print(file)
        text = str((pytesseract.image_to_string(Image.open(folder + "/" + file), lang='rus')))
        print(text)
        if "Температура" in text:
            if count_files == 1:
                Это утренний ковид журнал. 
                Переместить в папку Ковид, преобразовать в PDF и отправить по почте. Адрес записан в настройках.
                date_ind = text.find(".2021")
                date = text[date_ind:date_ind + 10]
                print(date)
                path_pdf = path_covid + "/" + date + "_" + get_config("company") + ".pdf"
                convert_2pdf(file, path_pdf)
                answer = mes.question(parent, "Сообщение", "Отправить ковидны журнал на почту " + to_email, mes.Ok | mes.Cansel)
                if answer == mes.Ok:
                    send_post(sub, body_text, to_email, path_pdf)
                pass
        elif "выдать" in text:
            create_note(parent, file, files)
        elif "разблокировать" in text:
            create_note(parent, file, files)
        elif "продлить " in text:
            create_note(parent, file, files)
        elif "ИТОГ" in text:
            date = next_bill(text, "B:\my_helper\scan\scan.jpg")
            return date
        elif "выходные" or "выходной" in text:
            create_note(parent, file, files)


def convert_2pdf(path_from, path_to):
    image = Image.open(path_from)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(path_to, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()

def create_note(parent, path, files):
    pdf_merger = PyPDF2.PdfFileMerger()
    output_file = "B:/my_helper/Служебки/Архив/PDF" + "1.pdf"
    for doc in files.sort():
        pdf_merger.append(str(doc))
    pdf_merger.write(output_file)
    answer = mes.question(parent, "Сообщение", "Отправаить ковидны журнал на почту " + to_email, mes.Ok | mes.Cansel)
    if answer == mes.Ok:
        send_post(sub, body_text, to_email, output_file)
    for doc in files:
        os.remove(doc)

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

"""