# Standard library imports
import os
import secrets

# Third party imports
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message

# Local application imports
from allocate import mail

def save_picture(form_picture, type: str):
    folder = 'avatars' if type == "user" else 'logos'
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', folder, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@stamper.com",
                  recipients=[user.email])
    msg.body = f'''W celu zresetowania hasła, kliknij w poniższy link
    {url_for('users.reset_token', token=token, _external=True)}

    Jeśli nie wnioskowałeś o reset hasła zignoruj tę wiadomość. Żadne zmiany nie zostaną wprowadozne'''

    mail.send(msg)