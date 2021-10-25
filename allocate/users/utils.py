# Standard library imports
import os
import secrets

# Third party imports
from flask import url_for, current_app
from PIL import Image

# Local application imports


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
