# thai-qr-payment
Generate QR Code image in the format of `Thai QR Payment`

- [KBANK](https://apiportal.kasikornbank.com/product/public/LandingPage/QR%20Payment/Introduction/3)


## Installation

available on pip https://pypi.org/project/thaiqrpayment/

```bash
pip install thaiqrpayment
```

## Usage

```python
import thaiqrpayment

# Your code from Bank
code = "01" * 100

# Save to image file
thaiqrpayment.save(code, "/tmp/qr.png")

# base64 format
base64_str = thaiqrpayment.to_base64(code)

# PIL image
pil_image = thaiqrpayment.generate(code)

```

## Example Image

![Thai QR Payment example](https://github.com/kittinan/thai-qr-payment/raw/main/assets/example.png?raw=true)