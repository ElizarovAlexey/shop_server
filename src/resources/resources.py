import os

from flask import request, send_from_directory, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

import config
from src.models.models import db
from src.models.models import Product, Category
from src.schemas.schemas import ProductSchema, CategorySchema


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


class ProductListApi(Resource):
    product_schema = ProductSchema()

    def get(self, uuid=None):
        """ Output a list, or a single film """
        if not uuid:
            products = db.session.query(Product).all()
            return self.product_schema.dump(products, many=True), 200

        product = db.session.query(Product).filter_by(uuid=uuid).first()

        if not product:
            return {'Error': 'Object was not found'}, 404

        return self.product_schema.dump(product), 200

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

        db.session.add(product)
        product.category_id = request.values['category_id']
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
