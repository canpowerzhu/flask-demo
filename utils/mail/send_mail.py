# @Author  : kane.zhu
# @Time    : 2023/2/8 19:37
# @Software: PyCharm
# @Description:
import os.path
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from settings.conf import PrdConfig


class SendMail(object):
    def __int__(self, sender, receiver, subject, is_attachment):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.is_attachment = is_attachment

    def send_verification_code_mail(self, msg):
        """
        :param msg: 发送html邮件类型的验证码
        :return: bool
        """
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = Header(self.sender, 'utf-8')
        message['To'] = Header(self.receiver)
        message['Subject'] = Header(self.subject, 'utf-8')
        try:
            mailobj = SMTP_SSL(PrdConfig.EMAIL_HOST, PrdConfig.EMAIL_SMTP_PORT)
            mailobj.login(PrdConfig.EMAIL_FROM_ACCOUNT, PrdConfig.EMAIL_FROM_ACCOUNT_PASS)
            mailobj.sendmail(PrdConfig.EMAIL_FROM_ACCOUNT, self.receiver, message.as_string())
            flag = True
        except smtplib.SMTPException:
            flag = False
        return flag

    def send_mail(self, body, appendix_file):
        msg = MIMEMultipart()
        if self.is_attachment and os.path.exists(appendix_file):
            msg.attach(MIMEText(body, 'plain'))
            attachment = open(appendix_file, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + appendix_file)

        # 判断是否批量发送
        receiver = ', '.join(self.receiver) if isinstance(self.receiver, list) else self.receiver

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP_SSL(PrdConfig.EMAIL_HOST, PrdConfig.EMAIL_SMTP_PORT)
        server.login(PrdConfig.EMAIL_FROM_ACCOUNT, PrdConfig.EMAIL_FROM_ACCOUNT_PASS)
        server.sendmail(self.sender, receiver, text)
        server.quit()
