import segno , io  

#- make QRcode
def make_qrcode(config_to_qrcode):
    QRcode = segno.make_qr(config_to_qrcode )
    image = io.BytesIO()
    QRcode.save(image , kind="png" ,  scale=15)
    image.seek(0)
    return image


