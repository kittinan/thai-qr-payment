from io import BytesIO
from PIL import Image

import base64
import qrcode
import os

__VERSION__ = "0.1.0"

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


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
