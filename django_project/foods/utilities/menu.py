def str_to_int(x):
    try:
        return int(x)
    except Exception:
        return None


def convert_to_recipe_id(a):
    ids = a.split(',')
    ids = map(str_to_int, ids)
    return tuple(filter(lambda x: x, ids))
