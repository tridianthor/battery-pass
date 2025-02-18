from django.forms import ValidationError


def validate_pdf_file(value):
    if not value.content_type.startswith('application/pdf'):
        """ raise ValidationError(
            message='Uploaded file is not a PDF.',
            code='invalid_file_type'
        ) """
        return False
    else:
        return True