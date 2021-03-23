import json
import random
from datetime import datetime
from faker import Faker

FOLDER = 'downloads/'
USER_DATA = FOLDER+'user.dat'
RECIPE_DATA = FOLDER+'recipe.jsonl'
REVIEW_DATA = FOLDER+'review.dat'

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

fake = Faker()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def preprocess_user_data(x):
    a = x.strip().split(',')
    try:
        a[0] = int(a[0])
        return a
    except:
        pass


def generate_auth_user(x):
    auth_user = {
        'password': HASHED_PASSWORD,
        'last_login': None,
        'is_superuser': False,
        'username': 'user_{}'.format(x[0]),
        'first_name': x[1],
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
        PK: x[0],
        FIELDS: auth_user
    }


def generate_food_user(x):
    foods_user = {
        'user': x[0],
        'birthday': BIRTHDAY,
        'height': fake.pyint(min_value=101, max_value=250),
        'weight': fake.pyint(min_value=20, max_value=200),
        'gender': fake.pybool(),
        'diet_factor': 1
    }
    return {
        MODEL: FOODS_USER,
        PK: x[0],
        FIELDS: foods_user
    }


def seed_user():
    with open(USER_DATA, 'r') as file:
        lines = file.readlines()
        a = list(map(preprocess_user_data, lines))
        auth_users = list(map(generate_auth_user, a))
        food_users = list(map(generate_food_user, a))
        return auth_users+food_users


def preprocess_recipe_data(x):
    r = json.loads(x)
    try:
        r['author'] = int(r['author'])
        r['recipe_id'] = int(r['recipe_id'])
        r['directions'] = list(map(lambda x: x.strip(), r['directions']))
        return r
    except Exception as e:
        print(e)


def generate_food_recipe(x):
    desc = '\n'.join(x['directions'])
    if len(desc) > 500:
        desc = desc[:500]
    full_name = x['full_name']
    if len(full_name) > 50:
        full_name = full_name[:50]
    recipe = {
        'user': x['author'],
        'dish_name': full_name,
        'description': desc,
        'calories': random.randint(10, 3000),
        'is_public': True,
        'ingredients': '',
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_DISH,
        PK: x['recipe_id'],
        FIELDS: recipe
    }


def seed_recipe():
    with open(RECIPE_DATA, 'r') as file:
        lines = file.readlines()
        a = list(map(preprocess_recipe_data, lines))
        return list(map(generate_food_recipe, a))


def preprocess_review_data(x):
    a = x.split(',')
    try:
        a[0] = int(a[0])
        a[1] = int(a[1])
        a[2] = int(a[2])
        a[3] = int(a[3])
        c = ','.join(a[4:])
        return a[0], a[1], a[2], a[3], c
    except Exception as e:
        print('Error:', e, a)


def generate_food_review(x):
    c = x[4]
    if len(c) > 100:
        c = c[:100]
    s = x[3]
    if s == 0:
        s = 0.5
    rv = {
        'user': x[2],
        'dish': x[1],
        'score': x[3],
        'comment': c,
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_RATING,
        PK: x[0],
        FIELDS: rv
    }


def seed_review():
    with open(REVIEW_DATA, 'r') as file:
        lines = file.readlines()
        a = list(map(preprocess_review_data, lines))
        a = list(filter(lambda x: x, a))
        return list(map(generate_food_review, a))


if __name__ == '__main__':
    # u = seed_user()
    # with open('u.json', 'w') as file:
    #     json.dump(u, file)
    # r = seed_recipe()
    # with open('r.json', 'w') as file:
    #     json.dump(r, file)
    rv = seed_review()
    with open('rv.json', 'w') as file:
        json.dump(rv, file)
