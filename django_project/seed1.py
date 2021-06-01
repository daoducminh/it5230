import json
import random
import pickle
from datetime import datetime
from faker import Faker

FOLDER = 'downloads/'
DATA = FOLDER + 'data.pkl'
FULL_FOLDER = FOLDER+'full/'
USER_DATA = FULL_FOLDER + 'users.pkl'
RECIPE_DATA = FULL_FOLDER + 'recipes.pkl'
REVIEW_DATA = FULL_FOLDER + 'review.pkl'
FOLLOW = FULL_FOLDER + 'follows.pkl'

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
AUTHOR_ID = 'author_id'
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
CATEGORY = 'category'
AUTHOR_URL = 'author_url'
USER_AVATAR_URL = 'user_avatar_url'

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


def generate_auth_user_by_id(x):
    auth_user = {
        'password': HASHED_PASSWORD,
        'last_login': None,
        'is_superuser': False,
        'username': 'user_{}'.format(x),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'is_staff': False,
        'is_active': True,
        'date_joined': DATE_JOINED,
        'groups': (),
        'user_permissions': ()
    }
    return {
        MODEL: AUTH_USER,
        PK: x,
        FIELDS: auth_user
    }


def generate_food_user_by_id(x):
    foods_user = {
        'user': x,
        'birthday': BIRTHDAY,
        'height': fake.pyint(min_value=101, max_value=250),
        'weight': fake.pyint(min_value=20, max_value=200),
        'gender': fake.pybool(),
        'diet_factor': 1
    }
    return {
        MODEL: FOODS_USER,
        PK: x,
        FIELDS: foods_user
    }


def seed_user(data):
    users = data[USER]
    auth_users = list(map(generate_auth_user, users))
    food_users = list(map(generate_food_user, users))
    u1 = {i[USER_ID] for i in users}
    u2 = {i[AUTHOR_ID] for i in data[RECIPE]}
    u3 = {i[USER_ID] for i in data[REVIEW]}
    s1 = u2-u1
    s2 = u3-u1
    a1 = []
    a2 = []
    for i in s1.union(s2):
        a1.append(generate_auth_user_by_id(i))
        a2.append(generate_food_user_by_id(i))
    return auth_users + food_users + a1 + a2


def handle_ingredients(x):
    return ' '.join(x.split())


def handle_url(x):
    a = x.strip()
    return a[1:-2]


def generate_food_recipe(x):
    ingredients = list(map(handle_ingredients, x[INGREDIENTS]))
    image_url = x.get(IMAGE_URL, '')
    desc = ' '.join(x[DIRECTIONS])
    if len(desc) > 5000:
        desc = desc[:5000]
    ing = ', '.join(ingredients)
    if len(ing) > 1000:
        ing = ing[:1000]
    recipe = {
        'user': x[AUTHOR_ID],
        'recipe_name': x[FULL_NAME],
        'description': desc,
        'calories': random.randint(10, 3000),
        'is_public': True,
        'ingredients': ing,
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
    c = x[COMMENT]
    if len(c) > 1000:
        c = c[:1000]
    c = c.replace('\x00', '')
    rv = {
        'user': x[USER_ID],
        'dish': x[RECIPE_ID],
        'score': x[RATING],
        'comment': c,
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_RATING,
        PK: x[REVIEW_ID],
        FIELDS: rv
    }


def seed_review(data):
    reviews = data[REVIEW]
    return list(map(generate_food_review, reviews))


def seed_combined_data():
    data = read_pickle(DATA)
    u = seed_user(data)
    with open('u1.json', 'w') as file:
        json.dump(u, file)
    r = seed_recipe(data)
    with open('r1.json', 'w') as file:
        json.dump(r, file)
    rv = seed_review(data)
    with open('rv1.json', 'w') as file:
        json.dump(rv, file)


def seed_split_data():
    u_data = read_pickle(USER_DATA)


if __name__ == '__main__':
    # seed_split_data()
    # seed_combined_data()
    data = read_pickle(DATA)
    print(data.keys())
