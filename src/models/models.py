import uuid
from src import db
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

products_sizes = db.Table(
    'products_sizes',
    db.Column('size_id', db.Integer, db.ForeignKey('sizes.id', ondelete="CASCADE"), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), primary_key=True)
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


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(120), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_image = db.Column(db.String(120), nullable=False)
    product_size = db.Column(db.Integer, nullable=False)
    product_count = db.Column(db.Integer, nullable=False)
    product_uuid = db.Column(db.String(36))

    def __init__(self, product_title, product_price, product_image, product_size, product_count, product_uuid):
        self.product_title = product_title
        self.product_price = product_price
        self.product_image = product_image
        self.product_size = product_size
        self.product_count = product_count
        self.product_uuid = product_uuid

    def __repr__(self):
        return f'Cart({self.product_title}, {self.product_price}, {self.product_size})'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    commentary = db.Column(db.String(120))

    items = db.Column(ARRAY(JSONB), default=[])

    def __init__(self, email, phone, name, city, total_price, commentary, items):
        self.email = email
        self.phone = phone
        self.name = name
        self.city = city
        self.total_price = total_price
        self.commentary = commentary
        self.items = items
