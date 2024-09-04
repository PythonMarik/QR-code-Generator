import qrcode
import base64
import re

from io import BytesIO
from flask import Flask, render_template, request

app = Flask(__name__)


# Проверка корректности ссылки
URL_REGEX = re.compile(
    "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
)


def validate_url(url):
    if not url:
        return False

    if re.match(URL_REGEX, url):
        return True


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate_qrcode():

    url = request.form.get("url")  # Ссылка от пользователя
    if not validate_url(url):
        return (
            render_template("error.html", message="Введите корректную ссылку!"),
            400,
        )  # Если неправильно введена ссылка

    # Генерируем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Создаем изображение
    img = qr.make_image(fill="black", back_color="white")

    # Сохраняем изображение в память
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Конвертируем изображение в base64 для отображения на странице
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Отправляем пользователю изображение
    return render_template("index.html", qr_code=img_base64)


if __name__ == "__main__":
    app.run(debug=True)
