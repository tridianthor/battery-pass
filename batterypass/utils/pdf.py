from django.http import HttpResponse


def view_pdf(request, filename, folder=None):
    if folder is None:
        with open(f'media/{filename}', 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
    else:
        with open(f'media/{folder}/{filename}', 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
    pdf.closed