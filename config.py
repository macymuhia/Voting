import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
    


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI='DATABASE_URL'
    DEBUG = False

class DevConfig(Config):
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
