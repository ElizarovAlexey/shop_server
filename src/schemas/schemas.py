from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.models.models import Product, Category, Size, Cart, Order, User


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
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

    sizes = Nested('SizeSchema', many=True)


class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_fk = True


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        load_only = ('password',)
