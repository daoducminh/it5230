import json
import random
from datetime import datetime
from faker import Faker

MODEL = 'model'
PK = 'pk'
FIELDS = 'fields'
AUTH_USER = 'auth.user'
FOODS_USER = 'foods.user'
FOODS_RECIPE = 'foods.recipe'
FOODS_RATING = 'foods.rating'
FOODS_CATEGORY = 'foods.category'
FOODS_MENU = 'foods.menu'
MENU_RATING = 'foods.menu_rating'
HASHED_PASSWORD = 'pbkdf2_sha256$216000$E7eK2AnWdjH7$vA0IUnEP2MzszO+Ubxp00DSiXq2AbT6wBDMex3XU00I='
DATE_JOINED = '2020-12-23T14:49:21+07:00'
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

CATEGORY_ADD_NAME = ['or', 'less']
RATING_STATS = 'rating_stats'
SCORE = 'score'
REVIEW_NUMBER = 'review_number'

INGREDIENT_LIST = ('ingredient 1', 'ingredient 2', 'ingredient 3')
DIRECTION_LIST = ('direction 1', 'direction 2', 'direction 3')

fake = Faker()
timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+07:00')


def write_json(obj, filename):
    with open(filename, 'w') as f:
        json.dump(obj, f)


def generate_auth_user(x, is_staff=False):
    if is_staff:
        username = f'admin_{x}'
    else:
        username = f'user_{x}'
    auth_user = {
        'password': HASHED_PASSWORD,
        'last_login': None,
        'is_superuser': False,
        'username': username,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'is_staff': is_staff,
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


def generate_food_user(x):
    foods_user = {
        'user': x,
        'birthday': BIRTHDAY,
        'gender': fake.pybool(),
        'image': '',
        'image_url': ''
    }
    return {
        MODEL: FOODS_USER,
        PK: x,
        FIELDS: foods_user
    }


def seed_user(n_admins=10, n_users=10):
    admin_range = range(1, n_admins + 1)
    staff_range = [True] * n_admins
    user_range = range(n_admins + 1, n_admins + n_users + 1)
    auth_admins = tuple(map(generate_auth_user, admin_range, staff_range))
    food_admin = tuple(map(generate_food_user, admin_range))
    auth_users = tuple(map(generate_auth_user, user_range))
    food_users = tuple(map(generate_food_user, user_range))
    return auth_admins + food_admin + auth_users + food_users, tuple(admin_range) + tuple(user_range)


def generate_food_recipe(x, user, category):
    recipe = {
        'user': user,
        'recipe_name': f'Recipe {x}',
        'description': 'Description',
        'directions': DIRECTION_LIST,
        'calories': random.randint(10, 3000),
        'ingredients': INGREDIENT_LIST,
        'image_url': '',
        'category': category,
        'total_time': random.randint(10, 100),
        'score': 0,
        'review_number': 0,
        'suggested': False,
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_RECIPE,
        PK: x,
        FIELDS: recipe
    }


def seed_recipe(users, categories, n_recipes=10):
    recipe_range = range(1, n_recipes + 1)
    user_rand = tuple(random.choice(users) for i in recipe_range)
    category_rand = tuple(random.choice(categories) for i in recipe_range)
    return tuple(map(generate_food_recipe, recipe_range, user_rand, category_rand)), tuple(recipe_range)


def generate_food_category(x):
    c = {
        'title': f'Category {x}',
        'short_name': f'category-{x}'
    }
    return {
        MODEL: FOODS_CATEGORY,
        PK: x,
        FIELDS: c
    }


def seed_category(n_categories=10):
    category_range = range(1, n_categories + 1)
    return tuple(map(generate_food_category, category_range)), tuple(category_range)


def generate_food_menu(x, user, recipes):
    m = {
        'user': user,
        'menu_name': f'Menu {x}',
        'description': 'Description',
        'score': 0,
        'review_number': 0,
        'created_at': timestamp,
        'updated_at': timestamp,
        'recipes': recipes
    }
    return {
        MODEL: FOODS_MENU,
        PK: x,
        FIELDS: m
    }


def seed_menu(users, recipes, n_menus=20):
    menu_range = range(1, n_menus + 1)
    user_rand = tuple(random.choice(users) for i in menu_range)
    menu_rand = tuple(random.sample(recipes, 5) for i in menu_range)
    return tuple(map(generate_food_menu, menu_range, user_rand, menu_rand)), tuple(menu_range)


def generate_recipe_review(x, user, recipe):
    rv = {
        'user': user,
        'recipe': recipe,
        'score': random.randint(1, 5),
        'comment': fake.text(100),
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: FOODS_RATING,
        PK: x,
        FIELDS: rv
    }


def seed_recipe_review(users, recipes, n_reviews=100):
    review_range = range(1, n_reviews + 1)
    user_rand = tuple(random.choice(users) for i in review_range)
    recipe_rand = tuple(random.choice(recipes) for i in review_range)
    return tuple(map(generate_recipe_review, review_range, user_rand, recipe_rand))


def generate_menu_review(x, user, menu):
    mv = {
        'user': user,
        'menu': menu,
        'score': random.randint(1, 5),
        'comment': fake.text(100),
        'created_at': timestamp,
        'updated_at': timestamp
    }
    return {
        MODEL: MENU_RATING,
        PK: x,
        FIELDS: mv
    }


def seed_menu_review(users, menus, n_reviews=100):
    review_range = range(1, n_reviews + 1)
    user_rand = tuple(random.choice(users) for i in review_range)
    menu_rand = tuple(random.choice(menus) for i in review_range)
    return tuple(map(generate_menu_review, review_range, user_rand, menu_rand))


if __name__ == '__main__':
    u_data, u_id = seed_user(10, 50)
    write_json(u_data, 'u.json')
    c_data, c_id = seed_category(20)
    write_json(c_data, 'c.json')
    r_data, r_id = seed_recipe(u_id, c_id, 500)
    write_json(r_data, 'r.json')
    m_data, m_id = seed_menu(u_id, r_id, 100)
    write_json(m_data, 'm.json')
    rv_data = seed_recipe_review(u_id, r_id, 500)
    write_json(rv_data, 'rv.json')
    mv_data = seed_menu_review(u_id, m_id, 500)
    write_json(mv_data, 'mv.json')
