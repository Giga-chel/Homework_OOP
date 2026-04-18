from unittest.mock import patch

import pytest

from src.main import Category, LawnGrass, BaseProduct, Product, Smartphone, Order, print_demo, BaseEntity


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def category_phones():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )


def test_product():
    product1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5


def test_category_init():
    phone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")
    phone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    phone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    category = Category(
        "Смартфоны",
        "Смартфоны для удобства",
        [phone1, phone2, phone3]
    )

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны для удобства"
    assert Category.category_count == 1
    assert Category.product_count == 3


def test_private_products_and_add_products():
    cat = Category("Телевизоры", "Описание")
    phone = Smartphone("Test Phone", "Описание", 50000.0, 2, 95.0, "Model", 128, "Black")

    with pytest.raises(AttributeError):
        _ = cat.__products

    cat.add_product(phone)
    assert Category.product_count == 1


def test_products_property_format(category_phones):
    products_list = category_phones.products

    assert len(products_list) == 3

    expected_str = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert products_list[0] == expected_str

    expected_str2 = "Iphone 15, 210000.0 руб. Остаток: 8 шт."
    assert products_list[1] == expected_str2


def test_new_product_classmethod():
    data = {"name": "Клавиатура", "description": "Механическая", "price": 5000.0, "quantity": 10}
    new_prod = Product.new_product(data)

    assert isinstance(new_prod, Product)
    assert new_prod.name == "Клавиатура"
    assert new_prod.price == 5000.0


def test_new_product_merge_and_max_price():
    existing_prod = Product("Клавиатура", "Механическая", 5000.0, 10)

    data_higher = {"name": "Клавиатура", "description": "Игровая", "price": 7000.0, "quantity": 5}
    merged_prod = Product.new_product(data_higher, [existing_prod])

    assert merged_prod is existing_prod
    assert merged_prod.quantity == 15
    assert merged_prod.price == 7000.0

    data_lower = {"name": "Клавиатура", "description": "Офисная", "price": 3000.0, "quantity": 2}
    merged_prod2 = Product.new_product(data_lower, [existing_prod])

    assert merged_prod2.quantity == 17
    assert merged_prod2.price == 7000.0


def test_product_setter_negative_price(capsys):
    prod = Product("Тест", "Тест", 100.0, 1)
    prod.price = -50.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert prod.price == 100.0


def test_product_setter_lower_price_confirm():
    prod = Product("Тест", "Тест", 100.0, 1)

    with patch("builtins.input", return_value="y"):
        prod.price = 80.0

    assert prod.price == 80.0


def test_product_setter_lower_price_reject():
    prod = Product("Тест", "Тест", 100.0, 1)

    with patch("builtins.input", return_value="n"):
        prod.price = 80.0

    assert prod.price == 100.0


def test_product_str():
    product = Product("TestProduct", "Описание", 1000.0, 5)
    assert str(product) == "TestProduct, 1000.0 руб. Остаток: 5 шт."


def test_category_str():
    cat = Category("Ноутбуки", "Техника", [])
    assert str(cat) == "Ноутбуки, количество продуктов: 0 шт."

    laptop = Smartphone("MacBook Pro", "Pro", 150000.0, 2, 95.0, "Model X", 512, "Silver")
    cat.add_product(laptop)
    assert str(cat) == "Ноутбуки, количество продуктов: 2 шт."


def test_product_add():
    product1 = Product("A", "Desc", 100.0, 2)
    product2 = Product("B", "Desc", 50.0, 4)

    result = product1 + product2
    assert result == 400
    assert isinstance(result, (int, float))


def test_product_add_zero_quantity():
    p1 = Product("A", "Desc", 100, 10)
    p2 = Product("B", "Desc", 50, 0)
    assert p1 + p2 == 1000


def test_category_iterator_loop(category_phones):
    collected_products = []

    for product in category_phones:
        assert isinstance(product, Product)
        collected_products.append(product.name)

    assert len(collected_products) == 3
    assert "Samsung Galaxy S23 Ultra" in collected_products
    assert "Iphone 15" in collected_products
    assert "Xiaomi Redmi Note 11" in collected_products


def test_category_iterator_manual():
    p1 = Product("A", "A", 10, 1)
    cat = Category("Cat", "Desc", [p1])

    iterator = iter(cat)

    assert next(iterator) == p1

    with pytest.raises(StopIteration):
        next(iterator)


def test_smartphone_creation():
    phone = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5, 3000, "S23 Ultra", 256, "Gray")
    assert phone.name == "Samsung Galaxy S23 Ultra"
    assert phone.efficiency == 3000
    assert phone.model == "S23 Ultra"
    assert phone.memory == 256
    assert phone.color == "Gray"


def test_lawn_grass_creation():
    grass = LawnGrass("Грубые травы", "Неприхотливая трава", 1500.0, 20, "Россия", 14, "Зеленый")
    assert grass.name == "Грубые травы"
    assert grass.country == "Россия"
    assert grass.germination_period == 14
    assert grass.color == "Зеленый"


def test_product_add_different_types():
    phone = Smartphone("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5, 3000, "S23 Ultra", 256, "Gray")
    grass = LawnGrass("Грубые травы", "Описание", 1500.0, 20, "Россия", 14, "Зеленый")

    with pytest.raises(TypeError):
        _ = phone + grass


def test_add_valid_products():
    phone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5, 3000, "S23 Ultra", 256, "Gray")
    phone2 = Smartphone("Iphone 15", "512GB", 210000.0, 8, 2800, "15", 512, "Gray")

    result = phone1 + phone2
    assert result == (phone1.price * phone1.quantity) + (phone2.price * phone2.quantity)

def test_abstract_class_creation_fail():
    with pytest.raises(TypeError):
        BaseProduct()