import os

class PrivateData(object):
    RAIN_TRASHOLD = 1 # 1mm/hour
    TLS_PORT = 587
    SMTP_SERVER = 'smtp.sendgrid.net'	

    def __init__(self):
        self.CITY_ID = os.environ['CITY_ID']
        self.APP_KEY = os.environ['APP_KEY'] 
        self.MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
        self.MAIL_USER_ACCOUNT = os.environ['MAIL_USER_ACCOUNT'] 
        self.MAIL_TO = os.environ['MAIL_TO'] 
        self.MAIL_FROM = os.environ['MAIL_FROM'] 
