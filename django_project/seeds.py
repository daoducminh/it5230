import random
from datetime import datetime
from json import dump

from faker import Faker

MODEL = 'model'
PK = 'pk'
FIELDS = 'fields'
USER_ID = 2

fake = Faker()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def seed_auth_user():
    model = 'auth.user'
    rs = []


def seed_food_dish():
    model = 'foods.dish'
    rs = []
    for i in range(1, 51):
        ingredients = []
        for j in range(5):
            ingredients.append(f'ingredient {random.randint(0, 1000)}')
        d = {
            'user': USER_ID,
            'dish_name': f'dish {i}',
            'description': fake.text(50),
            'calories': random.randint(10, 3000),
            'is_public': fake.pybool(),
            'ingredients': ','.join(ingredients)
        }
        rs.append({
            MODEL: model,
            PK: i,
            FIELDS: d
        })
    return rs


def seed_food_menu():
    model = 'foods.menu'
    rs = []
    for i in range(1, 11):
        dishes = []
        for j in range(8):
            dishes.append(random.randint(1, 50))
        m = {
            'user': USER_ID,
            'description': fake.text(50),
            'mealtime': timestamp,
            'limit': random.randint(3000, 10000),
            'dishes': dishes
        }
        rs.append({
            MODEL: model,
            PK: i,
            FIELDS: m
        })
    return rs


def seed_food_rating():
    model = 'foods.rating'
    rs = []
    for i in range(1, 51):
        r = {
            'user': USER_ID,
            'dish': i,
            'score': random.randint(1, 5),
            'comment': fake.text(50),
            'timestamp': timestamp
        }
        rs.append({
            MODEL: 'foods.rating',
            PK: i,
            FIELDS: r
        })
    return rs


if __name__ == '__main__':
    a = seed_food_dish()
    a += seed_food_rating()
    a += seed_food_menu()
    with open('foods.json', 'w') as file:
        dump(a, file)
