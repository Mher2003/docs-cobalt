import qrcode
import urllib
import io
import base64

def qr_create(base_url, type, file):
    qr_code = qrcode.make(urllib.parse.urljoin(base_url,type+"/"+file))
    byte_io = io.BytesIO()
    qr_code.save(byte_io)
    
    base64_image = base64.b64encode(byte_io.getvalue()).decode("utf-8")

    return base64_image