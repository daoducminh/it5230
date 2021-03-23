import json
import random
import pickle
from datetime import datetime
from faker import Faker

FOLDER = 'downloads/'
DATA = FOLDER + 'data.pkl'

MODEL = 'model'
PK = 'pk'
FIELDS = 'fields'
AUTH_USER = 'auth.user'
FOODS_USER = 'foods.user'
FOODS_DISH = 'foods.dish'
FOODS_RATING = 'foods.rating'
HASHED_PASSWORD = 'pbkdf2_sha256$216000$E7eK2AnWdjH7$vA0IUnEP2MzszO+Ubxp00DSiXq2AbT6wBDMex3XU00I='
DATE_JOINED = '2020-12-23T14:49:21Z'
BIRTHDAY = '2000-01-01'

RECIPE = 'recipe'
USER = 'user'
ERROR = 'error'
REVIEW = 'review'
URL = 'url'
TYPE = 'type'

RECIPE_ID = 'recipe_id'
SHORT_NAME = 'short_name'
FULL_NAME = 'full_name'
AUTHOR = 'author'
INGREDIENTS = 'ingredients'
DIRECTIONS = 'directions'
DETAIL = 'detail'
IMAGE_URL = 'image_url'
DESCRIPTION = 'description'
FACTS_TIME = 'facts_time'
FACTS_SERVES = 'facts_serves'
REVIEW_COUNT = 'review_count'
RATING = 'rating'
COMMENT = 'comment'
REVIEW_ID = 'review_id'

USERNAME = 'username'
FOLLOWER = 'follower'
FOLLOWING = 'following'
USER_ID = 'user_id'
FOLLOW = 'follow'

SCRIPT = 'script'

fake = Faker()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def read_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def generate_auth_user(x):
    auth_user = {
        'password': HASHED_PASSWORD,
        'last_login': None,
        'is_superuser': False,
        'username': 'user_{}'.format(x[USER_ID]),
        'first_name': x[USERNAME],
        'last_name': '',
        'email': fake.email(),
        'is_staff': False,
        'is_active': True,
        'date_joined': DATE_JOINED,
        'groups': (),
        'user_permissions': ()
    }
    return {
        MODEL: AUTH_USER,
        PK: x[USER_ID],
        FIELDS: auth_user
    }


def generate_food_user(x):
    foods_user = {
        'user': x[USER_ID],
        'birthday': BIRTHDAY,
        'height': fake.pyint(min_value=101, max_value=250),
        'weight': fake.pyint(min_value=20, max_value=200),
        'gender': fake.pybool(),
        'diet_factor': 1
    }
    return {
        MODEL: FOODS_USER,
        PK: x[USER_ID],
        FIELDS: foods_user
    }


def seed_user(data):
    users = data[USER]
    auth_users = list(map(generate_auth_user, users))
    food_users = list(map(generate_food_user, users))
    return auth_users + food_users


def handle_ingredients(x):
    return ' '.join(x.split())


def handle_url(x):
    a = x.strip()
    return a[1:-2]


def generate_food_recipe(x):
    ingredients = list(map(handle_ingredients, x[INGREDIENTS]))
    image_url = None
    if SCRIPT in x:
        a = x[SCRIPT].split('photoUrl: ')
        a = list(filter(lambda x: x, a))
        a = list(map(handle_url, a))
        image_url = a[0]
        if len(a[0]) < 100:
            image_url = a[0]
    recipe = {
        'user': x[AUTHOR],
        'dish_name': x[FULL_NAME],
        'description': ' '.join(x[DIRECTIONS]),
        'calories': random.randint(10, 3000),
        'is_public': True,
        'ingredients': ', '.join(ingredients),
        'image_url': image_url,
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_DISH,
        PK: x['recipe_id'],
        FIELDS: recipe
    }


def seed_recipe(data):
    recipes = data[RECIPE]
    return list(map(generate_food_recipe, recipes))


def generate_food_review(x):
    r = x[REVIEW]
    rv = {
        'user': r[USER_ID],
        'dish': r[REVIEW_ID],
        'score': r[RATING],
        'comment': r[COMMENT],
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_RATING,
        PK: r[REVIEW_ID],
        FIELDS: rv
    }


def seed_review(data):
    reviews = data[REVIEW]
    return list(map(generate_food_review, reviews))


if __name__ == '__main__':
    data = read_pickle(DATA)
    u = seed_user(data)
    r = seed_recipe(data)
    rv = seed_review(data)
    with open('data1.json', 'w') as file:
        json.dump(u+r+rv, file)
