from pyzbar import pyzbar
import cv2

def get_text(image_name):
    image = cv2.imread(image_name)

    barcodes = pyzbar.decode(image)

    outputs = []
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        outputs.append((barcodeType, barcodeData))

    return outputs
