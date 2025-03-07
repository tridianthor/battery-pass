from django.forms import ValidationError
from django.utils.translation import gettext as _

import json
import re

def validate_pdf_file(value):
    if not value.content_type.startswith('application/pdf'):
        """ raise ValidationError(
            message='Uploaded file is not a PDF.',
            code='invalid_file_type'
        ) """
        return False
    else:
        return True

def validate_json(value):
    try:
        json.loads(f'{value}')
    except ValueError as e:
        return ValidationError(_(f'Invalid JSON format'))

def validate_password_complexity(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_-]', password):
        raise ValidationError("Password must contain at least one special character.")