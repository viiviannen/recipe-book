import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # secret key is to protect against CSRF attacks in forms, useful to generate signatures or tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-mailtrap-username'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-mailtrap-password'
    ADMINS = ['example@example.com']
