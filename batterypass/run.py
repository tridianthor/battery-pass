from generalproductinfo.models import GeneralProductInformation, regenerate_qr_code

product = GeneralProductInformation.objects.get(battery_passport_identifier="battery-16964710060663")

regenerate_qr_code(product.id)