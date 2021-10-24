import os
import smtplib
import sys
from configparser import ConfigParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import logging
from database import DataBase, get_path, get_path_ui
logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)


def send_post(subject, body_text, to_email, file_to_attach):

    base_path = os.path.dirname(conf.path + conf.path_to_covid)
    config_path = os.path.join(base_path, "email.ini")
    header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach

    # get the config
    if os.path.exists(conf.path_conf_ini):
        cfg = ConfigParser()
        cfg.read(conf.path_conf_ini)
    else:
        print("Config not found! Exiting!")
        return False

    # extract server and from_addr from config
    host = cfg.get("smtp", "server")
    from_addr = cfg.get("smtp", "from_addr")

    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    if body_text:
        msg.attach(MIMEText(body_text))

    attachment = MIMEBase('application', "octet-stream")

    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()

        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_to_attach
        print(msg)
        return False

    server = smtplib.SMTP(host)
    server.sendmail(from_addr, to_email, msg.as_string())
    server.quit()
    return True
