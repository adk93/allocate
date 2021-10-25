
class Config:
    MAX_CONTENT_LENGTH = 8192 * 8192
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.pdf']
    SECRET_KEY = 'Thisissupposedtobesecret!'
    UPLOAD_PATH = 'uploads'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    LOGIN_DISABLED = False
    SECURITY_PASSWORD_SALT = 'thisisasecretsalt'
