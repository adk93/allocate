import os

class Config:
    MAX_CONTENT_LENGTH = 8192 * 8192
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.pdf']
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOAD_PATH = 'uploads'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    LOGIN_DISABLED = False
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
