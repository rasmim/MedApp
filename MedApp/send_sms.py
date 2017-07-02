from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACd122e1071a5af95d2bfda14f9af01c14"
auth_token = "a0add14b0047f41035ad142d60f630e8"
client = Client(account_sid, auth_token)

def send_sms(no_to='', no_from='', body=''):
    message = client.messages.create(to=no_to, from_=no_from, body=body)
        # to="+40784348384", from_="+17603137403",; body="Dr. Livia you have a new appointment at ")




    # iwbmejloqhxlbcac ------MedApp ---Gmail Pw

# tmedapp@gmail.com -------- Logitech123


