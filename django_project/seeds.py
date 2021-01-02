import random
from datetime import datetime
from json import dump

from faker import Faker

MODEL = 'model'
PK = 'pk'
FIELDS = 'fields'
USER_ID = 2
AUTH_USER = 'auth.user'
FOODS_USER = 'foods.user'
FOODS_DISH = 'foods.dish'
FOODS_RATING = 'foods.rating'
HASHED_PASSWORD = 'pbkdf2_sha256$216000$E7eK2AnWdjH7$vA0IUnEP2MzszO+Ubxp00DSiXq2AbT6wBDMex3XU00I='
DATE_JOINED = '2020-12-23T14:49:21Z'

fake = Faker()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


pool = {
    'vn-1': ['phở', 'bún', 'bầu', 'trứng', 'cá bạc má', 'cá chép', 'chim cút', 'gan heo', 'mướp', 'bơ', 'đậu hũ', 'bánh bao', 'bông cải', 'mỡ hành', 'cá cơm', 'bột', 'cá mòi', 'cà ri', 'cà tím', 'canh', 'canh khổ qua', 'cơm', 'xả ớt', 'đùi gà', 'gỏi', 'hủ tiếu', 'nấm rơm', 'bánh', 'phở', 'mì', 'cháo', 'chay', 'tôm lăn bột', 'bánh canh', 'vịt'],
    'vn-2': ['xào', 'chiên', 'chưng', 'tương', 'bò', 'riêu cua', 'nhồi thịt', 'chay', 'thập cẩm', 'thịt nướng', 'kho', 'gà', 'nướng', 'chua', 'nhồi thịt', 'rau ngót', 'chiên giòn', 'bắp chuối', 'ngó sen', 'bò kho', 'chiên xù', 'cua', 'mắm', 'măng', 'mọc', 'ốc', 'đậu đỏ', 'pía'],
    'ing': ['bầu', 'trứng gà', 'trứng vịt', 'hành', 'ngò', 'tôm', 'củ sắn', 'lạp xướng', 'xà lách', 'rau thơm', 'bánh tráng', 'lạc rang', 'cá bạc má', 'tiêu xay', 'hành lá', 'cá diêu hồng', 'mộc nhĩ', 'cần tây', 'cà chua', 'hành tây', 'bún tàu', 'rau sống', 'chim cút', 'bột cà ri', 'ngũ vị hương', 'tỏi', 'hành tím', 'gan heo', 'mướp hương', 'nấm rơm', 'giá đỗ', 'thịt thăn bò', 'nấm kim', 'nấm hương', 'cà tốt', 'bún', 'thịt bắp bò', 'giò heo', 'cua đồng', 'thịt xay', 'tôm', 'đậu hũ', 'bột bánh bao', 'tôm khô', 'nấm mèo', 'sườn chay', 'bông cải xanh', 'đậu hà lan', 'nấm đông cô', 'thịt heo', 'chả giò', 'bún tươi', 'bún gạo', 'cải ngọt', 'đậu phộng', 'cá cơm', 'bột mì', 'trứng', 'dưa muối', 'cá mòi', 'thịt ba chỉ', 'khoai tây', 'ớt', 'cà tím', 'cá lóc', 'thơm', 'dọc mùng', 'giá đậu', 'khổ qua', 'thịt xay', 'hành củ', 'rau ngót', 'tôm sú', 'cơm', 'đậu hà lan', 'sả', 'đùi gà', 'bột chiên giòn', 'bắp chuối', 'dưa chuột', 'ngó sen', 'rau răm', 'thịt nạm bò', 'thịt ba rọi', 'cua biển', 'chân giò', 'xương heo', 'con mực', 'ngò rí', 'con vịt', 'măng tươi', 'sườn non', 'chả lụa', 'giò sống', 'gạo tẻ', 'dừa nạo', 'mì tôm', 'cải thìa', 'bột bánh bò', 'dừa tươi', 'lá dứa'],
    'en': ['Fresh Spring Rolls', 'Maine', 'Lobster', 'Lasagna', 'Honey', 'Walnut', 'Shrimp', 'Fra Diavolo Sauce', 'Pasta', 'Crab Cakes', 'Scallops', 'Orleans Creole', 'Gumbo', 'Scampi', 'Baked', 'Pinakbet', 'Bringhe', 'Curry', 'Fried Rice', 'Coconut Curry', 'Tofu', 'Sweet Potato Soup', 'Vegan Thai Curry', 'Thai Green Curry', 'Chicken', 'Basic Mashed Potatoes', 'Apple Pie', 'Grandma Ople', 'Banana Bread', 'Pancakes', 'Homemade Mac', 'Cheese', 'Fried Rice', 'Crab-Stuffed', 'Mushrooms', 'Grilled Onions', 'Cheese Stuffed Mushrooms', 'Tennessee Meatloaf', 'Ordinary Meatloaf', 'Meat Pie', 'Southern Version', 'Treasures Ranch Pockets', 'Summer Feta Burger', 'Gourmet Cheese Spread']
}


def seed_user():
    auth_users = []
    foods_users = []
    for i in range(1, 21):
        gender = fake.pybool()
        auth_admin = {
            'password': HASHED_PASSWORD,
            'last_login': None,
            'is_superuser': True,
            'username': 'admin{}'.format(i),
            'first_name': fake.first_name_male() if gender else fake.first_name_female(),
            'last_name': fake.last_name_male() if gender else fake.last_name_female(),
            'email': 'johndoe@gmail.com',
            'is_staff': True,
            'is_active': True,
            'date_joined': DATE_JOINED,
            'groups': (),
            'user_permissions': ()
        }
        foods_user = {

        }


def seed_food_dish():
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
            'ingredients': ','.join(ingredients),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        rs.append({
            MODEL: FOODS_DISH,
            PK: i,
            FIELDS: d
        })
    return rs


def seed_food_rating():
    rs = []
    for i in range(1, 51):
        r = {
            'user': USER_ID,
            'dish': i,
            'score': random.randint(1, 5),
            'comment': fake.text(50),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        rs.append({
            MODEL: FOODS_RATING,
            PK: i,
            FIELDS: r
        })
    return rs


if __name__ == '__main__':
    a = seed_food_dish()
    a += seed_food_rating()
    with open('foods.json', 'w') as file:
        dump(a, file)
