import uuid
from src import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    uuid = db.Column(db.String(36), unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, title, price, image):
        self.title = title
        self.price = price
        self.image = image
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Product({self.title}, {self.price}, {self.uuid})'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    products = db.relationship('Product', backref="categories", lazy='dynamic')

    def __repr__(self):
        return '<Category("{}")'.format(self.name)
