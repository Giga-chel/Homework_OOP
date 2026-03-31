import pytest
from pathlib import Path
from src.main import Category, Product
from src.utils import load_json_data

@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0

def test_load_json_data():
    test_file_path = Path(__file__).parent / "test_data.json"

    categories = load_json_data(test_file_path)

    assert isinstance(categories, list)
    assert len(categories) == 1

    test_category = categories[0]
    assert isinstance(test_category, Category)
    assert test_category.name == "Тестовая категория"
    assert test_category.description == "Тестовое описание категории"

    assert len(test_category.products) == 1
    test_product = test_category.products[0]

    assert isinstance(test_product, Product)
    assert test_product.name == "Тестовый товар"
    assert test_product.price == 100.0
    assert test_product.quantity == 5

    assert Category.category_count == 1
    assert Category.product_count == 1
