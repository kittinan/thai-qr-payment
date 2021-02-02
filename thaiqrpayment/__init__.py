from io import BytesIO
from PIL import Image

import base64
import qrcode
import os
import re
from decimal import *
import crc16

__VERSION__ = "0.1.0"

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

ID_PAYLOAD_FORMAT = '00'
ID_POI_METHOD = '01'
ID_MERCHANT_INFORMATION_BOT = '29'
ID_TRANSACTION_CURRENCY = '53'
ID_TRANSACTION_AMOUNT = '54'
ID_COUNTRY_CODE = '58'
ID_CRC = '63'

PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE = '01'
POI_METHOD_STATIC = '11'
POI_METHOD_DYNAMIC = '12'
MERCHANT_INFORMATION_TEMPLATE_ID_GUID = '00'
BOT_ID_MERCHANT_PHONE_NUMBER = '01'
BOT_ID_MERCHANT_TAX_ID = '02'
BOT_ID_MERCHANT_EWALLET_ID = '03'
GUID_PROMPTPAY = 'A000000677010111'
TRANSACTION_CURRENCY_THB = '764'
COUNTRY_CODE_TH = 'TH'

def generate(code):

    # TODO: mode: color or black-white

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1
    )
    qr.add_data(code)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert("RGB")

    # Add Logo
    logo_img = Image.open("{}/assets/logo.png".format(SCRIPT_PATH))
    template_img = Image.open("{}/assets/template.png".format(SCRIPT_PATH))

    # Center log image
    pos = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)
    qr_img.paste(logo_img, pos, mask=logo_img.split()[3])

    # Resize for template
    qr_img = qr_img.resize((750, 750))

    # paste qr image to template
    pos = (125, 407)
    template_img.paste(qr_img, pos)

    thaiqr_img = template_img.convert("RGB")
    return thaiqr_img


def save(code, path):

    img = generate(code)
    img.save(path)


def to_base64(code, include_uri=False):

    img = generate(code)

    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if include_uri:
        return "data:image/png;base64," + img_str

    return img_str


def generate_code_from_mobile(number, amount):
    input = sanitize_input(number)
    pp_type = BOT_ID_MERCHANT_EWALLET_ID if len(input) >= 15 else BOT_ID_MERCHANT_TAX_ID if len(input) >= 13 else BOT_ID_MERCHANT_PHONE_NUMBER 
    pp_payload = generate_txt(ID_PAYLOAD_FORMAT, PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE)
    pp_amount_type = generate_txt(ID_POI_METHOD, POI_METHOD_DYNAMIC if amount else POI_METHOD_STATIC)
    pp_merchant_info = generate_txt(ID_MERCHANT_INFORMATION_BOT,generate_txt(MERCHANT_INFORMATION_TEMPLATE_ID_GUID, GUID_PROMPTPAY) + generate_txt(pp_type, format_input(input) ))
    pp_country_code = generate_txt(ID_COUNTRY_CODE, COUNTRY_CODE_TH)
    pp_currency = generate_txt(ID_TRANSACTION_CURRENCY, TRANSACTION_CURRENCY_THB)
    pp_decimal_value = (amount if is_positive_decimal(amount) else 0) and generate_txt(ID_TRANSACTION_AMOUNT, format_amount(amount))
    raw_data = pp_payload + pp_amount_type + pp_merchant_info + pp_country_code + pp_currency + pp_decimal_value + ID_CRC + '04' 
    return raw_data + str.upper(hex(crc16.crc16xmodem(raw_data.encode('ascii'),0xffff)).replace('0x',''))


def sanitize_input(input):
    return re.sub(r'(\D.*?)', '', input)


def generate_txt(id, value):
    return id + str(len(value)).zfill(2) + value


def format_input(id):
    numbers = sanitize_input(id)
    if len(numbers) >= 13: return numbers
    return (re.sub(r'^0', '66', numbers)).zfill(13)


def format_amount(amount):
    TWOPLACES = Decimal(10) ** -2
    return str(Decimal(amount).quantize(TWOPLACES))


def is_positive_decimal(n):
    try:
        a = float(n)
    except ValueError:
        return False
    else:
        return True if a > 0 else False
