from django.http import HttpResponse


def view_pdf(request, folder, filename):
    with open(f'{folder}/{filename}', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed