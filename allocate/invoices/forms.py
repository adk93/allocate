# Standard library imports
import os

# Third party imports
from wtforms import StringField,PasswordField, Form, IntegerField, MultipleFileField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, ValidationError
from flask_wtf.file import FileAllowed

# Local application imports
from werkzeug.utils import secure_filename


class InvoiceUploadForm(Form):
    files = MultipleFileField('invoices', validators=[FileAllowed(['pdf','png','pdf'])])

    def get_secure_filename(self) -> str:
        secure_filenames = []

        for file in self.files:
            sec_filename = secure_filename(file.filename)
            secure_filenames.append(sec_filename)

        return secure_filenames