import json

from src.main import Product, Category

def load_json_data(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories_list = []

    for category in data:
        new_category = Category(category['name'], category['description'])
        product_dict = category["products"]
        for product in product_dict:
            commodity = Product(product['name'], product['description'], product['price'], product['quantity'])
            new_category.add_product(commodity)
        categories_list.append(new_category)
    return categories_list