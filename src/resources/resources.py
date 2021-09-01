import datetime
import os
from functools import wraps

import jwt
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import config
from src.models.models import db, Size, products_sizes, Cart, Order, User
from src.models.models import Product, Category
from src.schemas.schemas import ProductSchema, CategorySchema, SizeSchema, CartSchema, OrderSchema, UserSchema


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        try:
            uuid = jwt.decode(token, config.SECRET_KEY)['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        user = db.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper


class ProductListApi(Resource):
    product_schema = ProductSchema()
    size_schema = SizeSchema()

    def get(self, uuid=None):
        """ Output a list, or a single film """
        page = request.args.get('page', default=1, type=int)
        category = request.args.get('category', default=0, type=int)
        per_page = 6
        total_records = db.session.query(Product).count()

        if not uuid:
            if category == 0:
                products = db.session.query(Product).paginate(page, per_page)
            else:
                products = db.session.query(Product).filter_by(category_id=category).paginate(page, per_page)
                total_records = db.session.query(Product).filter_by(category_id=category).count()
            return {
                       'products': self.product_schema.dump(products.items, many=True),
                       'total_records': total_records
                   }, 200

        product = db.session.query(Product).filter_by(uuid=uuid).first()
        sizes = db.session.query(products_sizes.columns.size_id).filter(product.id == products_sizes.columns.product_id)
        sizes_values = []
        for row in sizes:
            size = db.session.query(Size).filter_by(id=row[0]).first()
            sizes_values.append(size)

        if not product:
            return {'Error': 'Object was not found'}, 404

        return {
            'product': self.product_schema.dump(product),
            'sizes': self.size_schema.dump(sizes_values, many=True)
        }

    def post(self):
        """ Adding a product """

        try:
            file = request.files['file']
            data = {}
            filename = ''

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(config.UPLOAD_FOLDER, filename))

            data['title'] = request.values['title']
            data['price'] = request.values['price']
            data['image'] = config.UPLOAD_FOLDER + '/' + filename
            product = self.product_schema.load(
                data, session=db.session)
        except ValidationError as e:
            return {'Error': str(e)}, 400

        product.category_id = request.values['category_id']

        size_ids = [int(item) for item in request.values.getlist('sizes')]
        sizes = []
        for size_id in size_ids:
            sizes.append(db.session.query(Size).filter_by(id=size_id).first())

        product.sizes.extend(sizes)

        db.session.add(product)
        db.session.commit()
        return self.product_schema.dump(product), 201

    def put(self, uuid):
        """ Changing a product """

        product = db.session.query(Product).filter_by(uuid=uuid).first()
        if not product:
            return {'Error': 'Object was not found'}, 404

        try:
            data = {}
            if len(request.files) != 0:
                file = request.files['file']
                if allowed_file(file.filename):
                    file = request.files['file']
                    os.remove(product.image)
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.UPLOAD_FOLDER, filename))
                    data['image'] = config.UPLOAD_FOLDER + '/' + filename
            else:
                data['image'] = product.image

            if request.values['in_stock'] is not None:
                data['in_stock'] = request.values['in_stock']
            else:
                data['in_stock'] = product.in_stock

            data['title'] = request.values['title']
            data['price'] = request.values['price']
            product = self.product_schema.load(data, instance=product, session=db.session)
        except ValidationError as e:
            return {'Error': str(e)}, 400

        db.session.add(product)
        db.session.commit()
        return self.product_schema.dump(product), 200

    def delete(self, uuid):
        """ Delete a product """

        product = db.session.query(Product).filter_by(uuid=uuid).first()
        if not product:
            return '', 404

        db.session.delete(product)
        db.session.commit()
        return {'Success': 'Deleted successfully'}, 200


class CategoriesListApi(Resource):
    category_schema = CategorySchema()

    def get(self):
        categories = db.session.query(Category).all()

        if not categories:
            return {'Error': 'Object was not found'}, 404

        return self.category_schema.dump(categories, many=True), 200


class SizesListApi(Resource):
    size_schema = SizeSchema()

    def get(self):
        sizes = db.session.query(Size).all()

        if not sizes:
            return {'Error': 'Object was not found'}, 404

        return self.size_schema.dump(sizes, many=True), 200


class CartApi(Resource):
    cart_schema = CartSchema()

    def get(self):
        """ Get a cart item """

        cart_items = db.session.query(Cart).all()
        total_price = 0

        for item in cart_items:
            total_price += item.product_count * item.product_price

        if not cart_items:
            return []

        return {
                   'total_price': total_price,
                   'items': self.cart_schema.dump(cart_items, many=True)
               }, 200

    def post(self):
        """ Add a cart item """

        try:
            req_data = self.cart_schema.dump(request.json)
            item = db.session.query(Cart).filter_by(product_uuid=req_data['product_uuid']).first()

            if item and item.product_size == req_data['product_size']:
                item.product_count += req_data['product_count']
                db.session.add(item)
            else:
                item = self.cart_schema.load(req_data, session=db.session)

        except ValidationError as e:
            return {'Error': str(e)}, 400

        db.session.add(item)
        db.session.commit()
        return self.cart_schema.dump(item), 201

    def put(self):
        """ Change a cart item """
        req_data = self.cart_schema.dump(request.json)

        cart_item = db.session.query(Cart).filter_by(id=req_data['id']).first()
        if not cart_item:
            return {'Error': 'Object was not found'}, 404

        try:
            cart_item = self.cart_schema.load(request.json, instance=cart_item, session=db.session)
        except ValidationError as e:
            return {'Error': str(e)}, 400

        db.session.add(cart_item)
        db.session.commit()
        return self.cart_schema.dump(cart_item), 200

    def delete(self, id):
        """ Delete a cart item """

        cart_item = db.session.query(Cart).filter_by(id=id).first()
        if not cart_item:
            return '', 404

        db.session.delete(cart_item)
        db.session.commit()
        return {'Success': 'Deleted successfully'}, 200


class OrderApi(Resource):
    order_schema = OrderSchema()

    @token_required
    def get(self):
        page = request.args.get('page', default=1, type=int)
        state = request.args.get('state', default='', type=str)
        per_page = 10
        total_records = db.session.query(Order).count()

        try:
            if state == '':
                orders = db.session.query(Order).paginate(page, per_page)
            else:
                orders = db.session.query(Order).filter_by(state=state).paginate(page, per_page)
                total_records = db.session.query(Order).filter_by(state=state).count()
            if not orders:
                return []
        except ValidationError as e:
            return {'Error': str(e)}, 400

        return {
                   'orders': self.order_schema.dump(orders.items, many=True),
                   'total_records': total_records
               }, 200

    def post(self):
        try:
            req_data = request.json

            order_item = self.order_schema.load(req_data, session=db.session)

        except ValidationError as e:
            return {'Error': str(e)}, 400

        db.session.add(order_item)
        Cart.query.delete()
        db.session.commit()

        return self.order_schema.dump(order_item), 201

    def put(self):
        """ Change an order item """
        req_data = request.json

        order_item = Order.query.get(req_data['id'])

        if not order_item:
            return {'Error': 'Object was not found'}, 404

        order_item.state = request.json['state']

        db.session.commit()
        return self.order_schema.dump(order_item), 200


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'Error': str(e)}

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'Error': 'Such user exists'}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        user = db.session.query(User).filter_by(username=auth.get('username', '')).first()
        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        token = jwt.encode(
            {
                'user_id': user.uuid,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
            }, config.SECRET_KEY
        )

        print('token', token.decode('utf-8'))

        return jsonify(
            {
                'token': token.decode('utf-8')
            }
        )

