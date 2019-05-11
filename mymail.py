import smtplib
import base64
from getpass import *
import templates
from login_details import *

# Extract Base64 encoding of image to embed in email
with open('Bahrain.jpg', 'rb') as image:
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read).decode()

def send_mail(ep_name, to, cc, bcc, name_of_user, email_id, pwd, template, epm_name=''):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_id, pwd)

        sent_from = f'{name_of_user} <{email_id}>'

        if template == 'welcome':
            email_text = templates.welcome_email(sent_from, ep_name, to, cc, image_64_encode)
        elif template == 'no epm':
            email_text = templates.no_epm_assigned(sent_from, epm_name, ep_name, to, cc)


        server.sendmail(sent_from, to + cc + bcc, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

if __name__ == "__main__":
    template = 'welcome'
    details = verify_passcode_get_details()
    name_of_user = details['name']
    email_id = details['email']
    pwd = details['email_pwd']

    #Make sure these are entered correctly
    epm_name = 'Isa'

    ep_name = 'Yun Tan'
    to = ['1784765768@qq.com']
    cc = ['']
    bcc = ['']

    send_mail(ep_name, to, cc, bcc, name_of_user, email_id, pwd, template, epm_name)
