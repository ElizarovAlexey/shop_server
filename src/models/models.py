import uuid
from src import db

products_sizes = db.Table(
    'products_sizes',
    db.Column('size_id', db.Integer, db.ForeignKey('sizes.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    uuid = db.Column(db.String(36), unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sizes = db.relationship('Size', secondary=products_sizes, lazy='dynamic',
                           backref=db.backref('products', lazy=True))

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


class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Size("{}")'.format(self.value)
