import re

LESS_NAME = ('or', 'less')
MORE_NAME = ('or', 'more')


def convert_category_title(x):
    name = re.sub(r'[^0-9a-zA-Z\s]', '', x)
    chunks = name.lower().split(' ')
    return '-'.join(chunks)
