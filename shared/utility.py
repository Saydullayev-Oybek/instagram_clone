import re
import threading
import phonenumbers
from decouple import Config

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from twilio.rest import Client

email_regex = re.compile(r"^[a-z0-9]+[\.'\-]*[a-z0-9]+@(gmail|googlemail)\.com$")
phone_regex = re.compile(r"^(\+|00)[1-9][0-9 \-\(\)\.]{7,32}$")

def check_email_or_phone(email_or_phone):
    # phone_num = phonenumbers.parse(email_or_phone)

    if re.fullmatch(email_regex, email_or_phone):
        email_or_phone = "email"

    elif re.fullmatch(phone_regex, email_or_phone):
        email_or_phone = "phone"

    else:
        data = {
            'success': False,
            'message': 'Email yoki telefoningiz notogri'
        }
        raise ValidationError(data)

    return email_or_phone


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()

def send_mail(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {'code': code}
    )
    Email.send_email(
        {
            'subject': 'Royxatdan otish',
            'to_email': email,
            'body': html_content,
            'content_type': "html"
        }
    )


def send_phone_code(phone_num, code):
    account_sid = Config('account_sid')
    auth_token = Config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Sizning tasdiqlash kodingiz {code}",
        from_='+998900713633',
        to=f"{phone_num}"
    )




