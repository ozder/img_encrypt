from flask import Flask, request, render_template
from PIL import Image, ImageDraw, ImageFont
import cv2
import random
import string
import toml

app = Flask(__name__)

# Konfigürasyon dosyasını yükle
config = toml.load('config.toml')

# Anahtarın ayar dosyasından alınması
KEY = config['APP']['EncryptionKey']

# Yasaklı kelimelerin ayar dosyasından alınması
forbidden_words = config['APP']['ForbiddenWords']

def encrypt_image(image):
    encrypted_data = bytearray()
    key_index = 0

    for byte in image.tobytes():
        encrypted_byte = byte ^ ord(KEY[key_index])
        encrypted_data.append(encrypted_byte)
        key_index = (key_index + 1) % len(KEY)

    return Image.frombytes(image.mode, image.size, bytes(encrypted_data))

def decrypt_image(image):
    decrypted_data = bytearray()
    key_index = 0

    for byte in image.tobytes():
        decrypted_byte = byte ^ ord(KEY[key_index])
        decrypted_data.append(decrypted_byte)
        key_index = (key_index + 1) % len(KEY)

    return Image.frombytes(image.mode, image.size, bytes(decrypted_data))

def perform_ocr(image):
    # Basit OCR işlemi yerine çekirdek OCR kütüphanelerini kullanmak için ilgili kodu ekleyebilirsiniz.
    pass

def check_forbidden_words(text):
    for word in forbidden_words:
        if word.lower() in text.lower():
            return True
    return False

def draw_rectangle(image, coordinates):
    draw = ImageDraw.Draw(image)
    draw.rectangle(coordinates, outline="red", width=3)
    del draw
    return image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    image_file = request.files['image']
    image = Image.open(image_file)
    encrypted_image = encrypt_image(image)
    encrypted_image.save("static/encrypted_image.png")
    return render_template('result.html', image_path='static/encrypted_image.png', key=KEY)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_image_file = request.files['encrypted_image']
    encrypted_image = Image.open(encrypted_image_file)
    decrypted_image = decrypt_image(encrypted_image)
    decrypted_image.save("static/decrypted_image.png")

    ocr_result = ""
    has_forbidden_words = False

    if has_forbidden_words:
        image_with_rectangles = draw_rectangle(decrypted_image.copy(), [(0, 0), decrypted_image.size])

        font = ImageFont.truetype("arial.ttf", 14)
        draw = ImageDraw.Draw(image_with_rectangles)
        draw.text((10, 10), ocr_result, fill="red", font=font)

        image_with_rectangles.save("static/decrypted_image_marked.png")
        return render_template('result.html', image_path='static/decrypted_image_marked.png', key=KEY, ocr_result=ocr_result, has_forbidden_words=has_forbidden_words)

    return render_template('result.html', image_path='static/decrypted_image.png', key=KEY, ocr_result=ocr_result, has_forbidden_words=has_forbidden_words)

if __name__ == '__main__':
    app.run(debug=True)
