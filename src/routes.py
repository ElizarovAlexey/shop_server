from src.resources.resources import ProductListApi, CategoriesListApi
from src import api

api.add_resource(ProductListApi, '/products', '/products/<uuid>', strict_slashes=False)
api.add_resource(CategoriesListApi, '/categories', strict_slashes=False)
