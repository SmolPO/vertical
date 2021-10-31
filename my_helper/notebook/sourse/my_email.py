import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from my_helper.notebook.sourse.database import get_from_ini
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