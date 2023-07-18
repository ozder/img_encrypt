from flask import Flask, request, render_template
from PIL import Image
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    image = request.files['image']

    img = Image.open(image)
    img_data = img.convert("RGB").tobytes()

    encrypted_data = bytearray()
    key_index = 0

    for byte in img_data:
        encrypted_byte = byte ^ ord(key[key_index])
        encrypted_data.append(encrypted_byte)
        key_index = (key_index + 1) % len(key)

    encrypted_img = Image.frombytes("RGB", img.size, bytes(encrypted_data))
    encrypted_img.save("static/encrypted_image.png")

    return render_template('result.html', image_path='static/encrypted_image.png', key=key)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = request.form.get('key')
    encrypted_image = request.files['encrypted_image']

    img = Image.open(encrypted_image)
    img_data = img.convert("RGB").tobytes()

    decrypted_data = bytearray()
    key_index = 0

    for byte in img_data:
        decrypted_byte = byte ^ ord(key[key_index])
        decrypted_data.append(decrypted_byte)
        key_index = (key_index + 1) % len(key)

    decrypted_img = Image.frombytes("RGB", img.size, bytes(decrypted_data))
    decrypted_img.save("static/decrypted_image.png")

    return render_template('result.html', image_path='static/decrypted_image.png')

if __name__ == '__main__':
    app.run(debug=True)
