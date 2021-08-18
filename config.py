import pathlib

BASE_DIR = pathlib.Path(__file__).parent

UPLOAD_FOLDER = 'static/photos'

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])


POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'Shop',
    'host': 'localhost'
}


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = True
