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

