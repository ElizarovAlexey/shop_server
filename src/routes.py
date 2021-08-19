from src.resources.resources import ProductListApi, CategoriesListApi, SizesListApi
from src import api

api.add_resource(ProductListApi, '/products', '/products/<uuid>', '/products<page>', strict_slashes=False)
api.add_resource(CategoriesListApi, '/categories', strict_slashes=False)
api.add_resource(SizesListApi, '/sizes', strict_slashes=False)
