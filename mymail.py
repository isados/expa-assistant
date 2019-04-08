import smtplib
import base64
from getpass import *
import templates
from login_details import *


def send_mail(ep_name, to, cc, bcc, name_of_user, email_id, pwd, no_epm = False, epm_name=''):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_id, pwd)

        sent_from = f'{name_of_user} <{email_id}>'

        # Extract Base64 encoding of image to embed in email
        with open('Bahrain.jpg', 'rb') as image:
            image_read = image.read()
            image_64_encode = base64.encodestring(image_read).decode()

        if no_epm:
            email_text = templates.no_epm_assigned(sent_from, epm_name, ep_name, to, cc)
        else:
            email_text = templates.welcome_email(sent_from, ep_name, to, cc, image_64_encode)


        server.sendmail(sent_from, to + cc + bcc, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

if __name__ == "__main__":
    no_epm = False
    details = verify_passcode_get_details()
    name_of_user = details['name']
    email_id = details['email']
    pwd = details['email_pwd']

    #Make sure these are entered correctly
    epm_name = 'Isa'

    ep_name = 'Alaeddine'
    to = ['p_4083c5c6c7b1df0966766fb051a89e0581d46cf3@inbound.aiesec.org']
    cc = ['p_5ccb228b24c9e1ec78ea0491e808f6e1cb12ad11@inbound.aiesec.org','p_229414617faf41e164c9a8a4353c83da9f9006f8@inbound.aiesec.org']
    bcc = []

    send_mail(ep_name, to, cc, bcc, name_of_user, email_id, pwd, no_epm, epm_name)
