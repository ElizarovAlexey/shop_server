from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.models.models import Product, Category, Size


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        exclude = ['id']
        load_instance = True
        include_fk = True

    category = Nested('CategorySchema', many=True)


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_fk = True

    category = Nested('CategorySchema', many=True)


class SizeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Size
        load_instance = True
        include_fk = True

    size = Nested('SizeSchema', many=True)
