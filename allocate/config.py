
class Config:
    MAX_CONTENT_LENGTH = 8192 * 8192
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.pdf']
    SECRET_KEY = 'Thisissupposedtobesecret!'
    UPLOAD_PATH = 'uploads'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    LOGIN_DISABLED = False
    SECURITY_PASSWORD_SALT = 'thisisasecretsalt'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kaminski.ad@gmail.com'
    MAIL_PASSWORD = 'dupa'
