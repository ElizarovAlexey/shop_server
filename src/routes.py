from src.resources.resources import ProductListApi, CategoriesListApi, SizesListApi, CartApi, OrderApi
from src import api

api.add_resource(ProductListApi, '/products', '/products/<uuid>', strict_slashes=False)
api.add_resource(CategoriesListApi, '/categories', strict_slashes=False)
api.add_resource(SizesListApi, '/sizes', strict_slashes=False)
api.add_resource(CartApi, '/cart', '/cart/<id>', strict_slashes=False)
api.add_resource(OrderApi, '/order', strict_slashes=False)
