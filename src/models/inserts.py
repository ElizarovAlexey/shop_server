from src import db
from src.models.models import Product, Category


def populate_films():
    chair = Product(
        title='Мужские кроссовки Jordan MA2',
        price=11990,
        image="https://sneakerhead.ru/upload/resize_cache/iblock/cbd/582_874_1/cbd67154876993bf34dae8bb2fcd5c23.jpg"
    )
    book = Product(
        title='Мужские кроссовки PUMA Suede Bloc WTFormstripe',
        price=8990,
        image="https://sneakerhead.ru/upload/resize_cache/iblock/a85/582_874_1/a85786e156e4455d4b532c6f6488476b.jpg"
    )
    computer = Product(
        title='Женские кроссовки Nike WMNS Air Force 1 07 SE',
        price=9490,
        image="https://sneakerhead.ru/upload/resize_cache/iblock/cbd/582_874_1/cbd67154876993bf34dae8bb2fcd5c23.jpg"
    )

    db.session.add(chair)
    db.session.add(book)
    db.session.add(computer)

    sport = Category(
        id=1,
        name='Спортивные'
    )

    classic = Category(
        id=2,
        name='Классические'
    )

    db.session.add(sport)
    db.session.add(classic)

    book.category_id = sport.id
    computer.category_id = sport.id
    chair.category_id = classic.id

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_films()
    print('Successfully populated!')


# from src.schemas.schemas import ProductSchema
#
# product_schema = ProductSchema()
#
# product = db.session.query(Product).all()
# print(product_schema.dump(product, many=True))
