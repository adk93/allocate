# Standard library imports
import os

# Third party imports

# Local application imports
from werkzeug.utils import secure_filename

def validate_uploaded_files(uploaded_files: list, app) -> tuple:
    invalid_extension_files = []
    valid_extension_files = []

    for uploaded_file in uploaded_files:
        sec_filename = secure_filename(uploaded_file.filename)
        filename = os.path.splitext(sec_filename)[1]
        if filename != "" and filename.lower() not in app.config['UPLOAD_EXTENSIONS']:
            invalid_extension_files.append(uploaded_file)
        else:
            valid_extension_files.append(uploaded_file)

    return valid_extension_files, invalid_extension_files

