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

    expected_str = "Тестовый товар, 100.0 руб. Остаток: 5 шт."
    assert test_product == expected_str

    assert Category.category_count == 1
    assert Category.product_count == 1
