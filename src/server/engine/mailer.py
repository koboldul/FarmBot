import smtplib

from email.mime.text import MIMEText
from engine.private_data import PrivateData

class Mailer:
	def __init__(self):
		self.smtpObj = smtplib.SMTP

		self.url = PrivateData.SMTP_SERVER
		self.port = int(PrivateData.TLS_PORT)

		self.private_data = PrivateData()

	def send_message(self, message, subject):
		m = MIMEText(message)
		m['Suject']= subject	
		self.send_mail(m)

	def send_mail(self, message):
		message['From'] = self.private_data.MAIL_FROM
		message['To'] = self.private_data.MAIL_TO
	
		try:
			smtpObj = smtplib.SMTP(self.url, self.port)
			smtpObj.starttls()
			smtpObj.login(self.private_data.MAIL_USER_ACCOUNT, self.private_data.MAIL_PASSWORD)
			smtpObj.sendmail(self.private_data.MAIL_FROM, self.private_data.MAIL_TO, message.as_string())         
			print ("Successfully sent email")
		except Exception as e:
			print (e)
			print ("Error: unable to send email")

