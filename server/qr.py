import qrcode
import urllib
import os

def CreateQR(baseURL, docsdir, id, type, file):
    img = qrcode.make(urllib.parse.urljoin(baseURL,type+"/"+file))
    img.save(os.path.join(docsdir,"QR",id+".png"))
    return True