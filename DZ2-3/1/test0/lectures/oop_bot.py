import random
from faker import Faker

fake = Faker()
fake.name()  # генерує випадкове імʼя

PRODUCT_NAMES = ("oil filter", "air filter", "engine oil", "transition oil", "bulb", "spark", "antifreeze")

class Suplier:
    def __init__(self, company_name, delivery_time) -> None:
        self.company_name = company_name
        self.delivery_time = delivery_time
        print(f"Suplier {self.company_name} was created")


class Product:
    def __init__(self, number, product_name, price_purchase, price_sales, supplier: Suplier) -> None:
        self.number = number
        self.product_name = product_name
        self.price_purchase = price_purchase
        self.price_sales = price_sales
        self.suplier = supplier
        # print(f"Product {self.product_name} was created")

    def __repr__(self) -> str:
        return f"{self.product_name} {self.number}"


class Car:
    def __init__(self, brand, model, year) -> None:
        self.brand = brand
        self.model = model
        self.year = year
        self.catalog: list[Product] = []
        print(f"Car {self.model} was added to Garage")

    def add_spare_part(self, parts: list[Product]):
        self.catalog.extend(parts)
        print(f"Spare parts was added {parts}")

    def __repr__(self) -> str:
        return f"{self.brand} {self.model} {self.year}"


class Warehouse:
    def __init__(self, location) -> None:
        self.location = location
        self.stock: list[Product] = []

    def products_feed(self, *args, volume=100):
        for item in range(volume):
            price_purchase = random.randint(1, 99)
            price_sales = round(price_purchase * 1.2, 2)
            product = Product(random.randint(1, 20), random.choice(PRODUCT_NAMES), price_purchase, price_sales,
                              random.choice(args))
            self.stock.append(product)

    def __repr__(self):
        return self.location


class Garage:
    def __init__(self, garage_name) -> None:
        self.garage_name = garage_name
        self.cars: list[Car] = []
        print(f"Garage {garage_name} was created")

    def add_car(self, *args: Car):
        for car in args:
            self.cars.append(car)
            print(f"Car was added {car}")

    def __repr__(self) -> str:
        return self.garage_name


class Bot:
    def __init__(self) -> None:
        self.user_dict = {}
        self.garages: list[Garage] = []
        self.warehouses: list[Warehouse] = []
        self.pagination = 5

    def add_service(self, garage: Garage):
        self.garages.append(garage)
        print(f"Garage {garage} was added to Bot")

    def add_warehouse(self, *args: Warehouse):
        for warehouse in args:
            self.warehouses.append(warehouse)
            print(f"Warehouse was added {warehouse}")

    def get_part_numbers_by_model(self, model):
        pass

    def get_variation_by_number(self, number):
        print(f"Number {number}")
        variations = []
        for garage in self.garages:
            for car in garage.cars:
                for product in car.catalog:
                    if product.number == number:
                        variations.append({"supplier": product.suplier.company_name, "number": product.number,
                                           "delivery": product.suplier.delivery_time, "price": product.price_sales})
        return variations

    def get_variation_by_number_on_stock(self, number, n=None):
        if n:
            self.pagination = n
        variations = []
        for warehouse in self.warehouses:
            for product in warehouse.stock:
                if product.number == number:
                    variations.append({"supplier": product.suplier.company_name, "number": product.number,
                                       "product name": product.product_name,
                                       "delivery": product.suplier.delivery_time, "price": product.price_sales})
        return self.__next__(variations)

    def __iter__(self, variations: list[dict]):
        temp_lst = []
        counter = 0

        for var in variations:
            temp_lst.append(var)
            counter += 1
            if counter >= self.pagination:
                yield temp_lst
                temp_lst.clear()
                counter = 0
        yield temp_lst

    def __next__(self, variations):
        generator = self.__iter__(variations)
        page = 1
        while True:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result = next(generator)
                    if result:
                        print(f"{'*' * 20} Page {page} {'*' * 20}")
                        page += 1
                    for var in result:
                        print(var)
                except StopIteration:
                    print(f"{'*' * 20} END {'*' * 20}")
                    break
            else:
                break


if __name__ == "__main__":
    # garage = Garage("Python Service")
    # work_car = Car("Volkswagen", "T4", 2000)
    # family_car = Car("Renault", "Megane 3", 2012)
    # garage.add_car(work_car, family_car)

    # automum = Suplier("AutoMum", "1 day")
    # emex = Suplier("Emex", "14 days")
    # elit = Suplier("Elit", "3 hours")

    # filter_oil_megan3 = Product("wix-1312", "Engine oil filter", 10.0, 12.99, automum)
    # engine_oil_megan3 = Product("elf500", "5w30", 32, 45.5, elit)
    # engine_oil_megan3_emex = Product("elf500", "5w30", 25, 38.5, emex)
    # spark_megan3 = Product("kh400", "Spark Irridium", 12, 15.75, elit)
    # family_car.add_spare_part([filter_oil_megan3, engine_oil_megan3, spark_megan3, ])

    # filter_oil_t4 = Product("man-900", "Diesel Engine oil filter", 13.0, 17.99, automum)
    # engine_oil_t4 = Product("Total-18", "10w40", 25, 30.5, elit)
    # spark_t4 = Product("tt400", "Spark Set", 30, 45.75, elit)
    # work_car.add_spare_part([filter_oil_t4, engine_oil_t4, spark_t4])

    # print(garage)

    # bot = Bot()
    # bot.add_service(garage)
    # variations = bot.get_variation_by_number("elf500")
    # for var in variations:
    #     print(var)

    """version 2"""
    bot = Bot()
    south_warehouse = Warehouse("Odesa")
    north_warehouse = Warehouse("Kyiv")

    automum = Suplier("AutoMum", "1 day")
    emex = Suplier("Emex", "14 days")
    elit = Suplier("Elit", "3 hours")

    south_warehouse.products_feed(automum, emex, elit, volume=100)
    north_warehouse.products_feed(automum, emex, elit, volume=120)

    bot.add_warehouse(south_warehouse, north_warehouse)

    bot.get_variation_by_number_on_stock(10, 4)

