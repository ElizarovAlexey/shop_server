import uuid

from werkzeug.security import generate_password_hash

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
    cart_items = db.relationship('Cart', backref="products", lazy="dynamic")

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_size = db.Column(db.Integer)
    product_count = db.Column(db.Integer)

    def __init__(self, user_id, product_id, product_size, product_count):
        self.user_id = user_id
        self.product_id = product_id
        self.product_size = product_size
        self.product_count = product_count

    def __repr__(self):
        return f'Cart({self.id, self.product_id})'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    commentary = db.Column(db.String(120))
    state = db.Column(db.String(30))
    date = db.Column(db.DateTime)

    items = db.Column(ARRAY(JSONB), default=[])

    def __init__(self, email, phone, name, city, total_price, commentary, items, date):
        self.email = email
        self.phone = phone
        self.name = name
        self.city = city
        self.total_price = total_price
        self.commentary = commentary
        self.items = items
        self.state = 'В обработке'
        self.date = date


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(36), unique=True)
    cart_items = db.relationship('Cart', backref="users", lazy="dynamic")

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.uuid})'
