from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from my_helper.notebook.sourse.database import *
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)


def send(subject, body_text, to_email, file_to_attach):
    server = get_from_ini("smtp", "post")
    user = get_from_ini("my_email", "post")
    password = get_from_ini("password", "post")

    recipients = to_email
    sender = user
    subject = subject
    text = body_text

    filepath = file_to_attach
    basename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipients

    part_text = MIMEText(text, 'plain')
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    part_file.set_payload(open(filepath, "rb").read())
    part_file.add_header('Content-Description', basename)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    encoders.encode_base64(part_file)

    msg.attach(part_text)
    msg.attach(part_file)

    mail = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    return

designer_file_email = get_path_ui("email")


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
            return True
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
        answer = mes.question(self, "Сообщение", "Отправить письмо на почту ? " + self.to_email,
                              mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            send(self.my_sub, self.body_text, self.to_email, self.path)
            self.close()

    def ev_cancel(self):
        self.close()

    def init_emails(self):
        try:
            rows = self.db.get_data("email", "bosses")
        except:
            mes.question(self, "Сообщение", my_errors["8_get_data"] + folder, mes.Cancel)
            return False
        for item in rows:
            print(item)
            self.email.addItem(item[0])

    def check_input(self):
        return True