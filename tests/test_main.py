import pytest
from src.main import Category, Product, print_demo

print_demo()

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
    return Category("Смартфоны", "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

def test_product():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5

def test_category_init(category_phones):
    assert category_phones.name == "Смартфоны"
    assert category_phones.description == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    assert Category.category_count == 1
    assert Category.product_count == 3

def test_private_products_and_add_products():
    cat = Category("Телевизоры", "Описание")
    prod = Product("Тест", "Описание", 100, 1)

    with pytest.raises(AttributeError):
        _ = cat.__products

    cat.add_product(prod)
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
