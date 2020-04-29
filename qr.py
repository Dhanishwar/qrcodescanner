import pyqrcode
import png
def qrgen(s):
    qr = pyqrcode.create(s)
    qr.png(s+'.png',scale = 8)
