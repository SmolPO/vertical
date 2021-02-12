import imap_tools as imap
import email
import configparser
import smtplib
import datetime
import datefinder

HOST_ = "mySMTP.server.com"

class MyEmail:
    def __init__(self):
        self.time_last_check = datetime.datetime.today()

    def connect_to_email(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.imap = self.config.get("post", "imap")
        self.login = self.config.get("post", "login")
        self.password = self.config.get("post", "password")
        self.inbox = self.config.get("post", "inbox")
        self.HOST = self.config.get("post", "smtp")

        self.mailbox = imap.MailBox(self.imap)
        self.mailbox.login(self.login, self.password, initial_folder=self.inbox)
        pass

    def close(self):
        self.mailbox.logout()

    def send_post(self, email_, sub, text, file=None):
        message = "\r\n".join((
            "From: %s" % self.login,
            "To: %s" % email_,
            "Subject: %s" % sub,
            "", text))
        server = smtplib.SMTP(self.HOST)
        server.sendmail(self.login, [email_], message)
        server.quit()
        pass

    def check_new_letters(self):
        result, data = self.mail.search(None, "ALL")
        pass

    def get_new_post(self):
        for msg in self.mailbox.fetch():
            if msg.is_new_post(msg):
                pass
        pass

    def is_new_post(self, msg):
        matches = next(datefinder.find_dates("original date - 'Tue, 03 Jan 2017 22:26:59 +0500'"))
        day = matches.day
        month = matches.month
        year = matches.year
        hour = matches.hour
        minute = matches.minute
        second = matches.second
        micro = matches.microsecond
        post_data = datetime.datetime(year, month, day, hour, minute, second, micro)
        now_data = datetime.datetime.today()

        delte_1 = now_data - self.time_last_check
        delte_2 = now_data - post_data
        delte = delte_1.seconds - delte_2.seconds

        if delte > 0:
            pass

matches = next(datefinder.find_dates("original date - 'Tue, 03 Jan 2017 22:26:59 +0500'"))
day = matches[0].day
month = matches[0].month
year = matches[0].year
hour = matches[0].hour
minute = matches[0].minute
second = matches[0].second
micro = matches[0].microsecond
new_data = datetime.datetime(year, month, day, hour, minute, second, micro)
now_data = datetime.datetime.now()
delte = new_data - now_data

print(mail.list())
mail.select("inbox") # Подключаемся к папке "входящие".
result, data = mail.search(None, "ALL")

ids = data[0]  # Получаем сроку номеров писем
id_list = ids.split()  # Разделяем ID писем
latest_email_id = id_list[1]  # Берем последний ID

result, data = mail.fetch(latest_email_id, "(RFC822)")  # Получаем тело письма (RFC822) для данного ID

raw_email = data[0][1]  # Тело письма в необработанном виде

import email

email_message = email.message_from_string(str(raw_email))

print (email_message['To'])
print (email.utils.parseaddr(email_message['From']))  # получаем имя отправителя "Yuji Tomita"
print(email_message.items())  # Выводит все заголовки.

def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

# включает в себя заголовки и альтернативные полезные нагрузки