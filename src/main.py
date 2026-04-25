from abc import ABC, abstractmethod


class BaseProduct(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def __str__(self):
        pass  # pragma: no cover


class MixinProduct:
    def __init__(self, *args, **kwargs):
        print(f"{self.__class__.__name__}{args}")
        super().__init__(*args, **kwargs)


class Product(MixinProduct, BaseProduct):
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = 0.0
        self.price = price
        self.quantity = quantity
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input("Понизить цену? y/n\n")
            if answer.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data, existing_products=None):
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if existing_products:
            for product in existing_products:
                if product.name == name:
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        return cls(name, description, price, quantity)

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать продукты разных категорий.")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency=None, model=None, memory=None, color=None):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class CategoryIterator:
    def __init__(self, category):
        self.products = category._Category__products
        self.index = 0

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration

    def __iter__(self):
        return self  # pragma: no cover


class BaseEntity(ABC):
    def __init__(self, name):
        self.name = name


class Order(BaseEntity):
    def __init__(self, name, product, quantity):
        super().__init__(name)
        self.product = product
        self.quantity = quantity

    @property
    def total_cost(self):
        return self.product.price * self.quantity


class Category(BaseEntity):
    category_count = 0
    product_count = 0

    name: str
    description: str
    __products: list

    def __init__(self, name, description, products=None):
        super().__init__(name)
        self.description = description
        self.__products = []

        if products is None:
            products = []

        for product in products:
            self.add_product(product)

        Category.category_count += 1

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Только продукты типа Smartphone или LawnGrass могут быть добавлены.")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self)

    @property
    def products(self):
        return [str(p) for p in self.__products]


def print_demo():  # pragma: no cover
    phone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    phone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    phone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    grass5 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass6 = LawnGrass("Газонная трава 2", "Выносливая травa", 450.0, 15, "США", "5 дней", "Темно-зеленый")
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [phone1, phone2, phone3],
    )
    category2 = Category("Газонная трава", "Различные виды газонной травы", [grass5, grass6])

    print(phone1.name)
    print(phone1.description)
    print(phone1.price)
    print(phone1.quantity)
    print(phone1.efficiency)
    print(phone1.model)
    print(phone1.memory)
    print(phone1.color)

    print(phone2.name)
    print(phone2.description)
    print(phone2.price)
    print(phone2.quantity)
    print(phone2.efficiency)
    print(phone2.model)
    print(phone2.memory)
    print(phone2.color)

    print(phone3.name)
    print(phone3.description)
    print(phone3.price)
    print(phone3.quantity)
    print(phone3.efficiency)
    print(phone3.model)
    print(phone3.memory)
    print(phone3.color)

    print(product4.name)
    print(product4.description)
    print(product4.price)
    print(product4.quantity)

    print(grass5.name)
    print(grass5.description)
    print(grass5.price)
    print(grass5.quantity)
    print(grass5.country)
    print(grass5.germination_period)
    print(grass5.color)

    print(grass6.name)
    print(grass6.description)
    print(grass6.price)
    print(grass6.quantity)
    print(grass6.country)
    print(grass6.germination_period)
    print(grass6.color)

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)


if __name__ == "__main__":
    print_demo()  # pragma: no cover
