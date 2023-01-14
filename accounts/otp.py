from django.conf import settings
from twilio.rest import Client
import random

class MessageHandler:

  phone_number = None
  otp = None

  def __init__(self,phone_number,otp) -> None:
    self.phone_number  = phone_number
    self.otp           = otp
    print("generated otp = ",self.otp)


  def send_otp(self):
    account_sid = settings.ACCOUNT_SID
    auth_token  = settings.AUTH_TOKEN
    client      = Client(account_sid,auth_token)
    verification = client.verify \
                .v2 \
                .services('VAf4cc193fe06bc90cff18866d5c1f1462') \
                .verifications \
                .create(to= self.phone_number,channel ='sms')


  def validate(self):
    account_sid = settings.ACCOUNT_SID
    auth_token  = settings.AUTH_TOKEN
    client      = Client(account_sid,auth_token)
    verification_check  = client.verify \
      .v2 \
      .services('VAf4cc193fe06bc90cff18866d5c1f1462')\
      .verification_checks \
      .create(to = self.phone_number,code = self.otp)

    validation = verification_check.status
    print(validation)
    return validation
      


