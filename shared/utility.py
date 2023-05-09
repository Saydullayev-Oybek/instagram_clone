import re
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"^[a-z0-9]+[\.'\-]*[a-z0-9]+@(gmail|googlemail)\.com$")
phone_regex = re.compile(r"(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$")

def check_email_or_phone(email_or_phone):
    if re.fullmatch(email_regex, email_or_phone):
        email_or_phone = "email"
    elif re.fullmatch(phone_regex, email_or_phone):
        email_or_phone = "phone"
    else:
        data = {
            'message': 'Email yoki telefoningiz notogri',
            'success': False
        }
        raise ValidationError(data)

    return email_or_phone