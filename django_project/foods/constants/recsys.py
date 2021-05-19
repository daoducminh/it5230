import pickle

FILENAME = 'recsys/{}.pkl'


def get_data(data='dataset', normalized=False, version=None):
    prefix = 'n_' if normalized else ''
    ver = f'_{version}' if version else ''
    dataset = f'{prefix}{data}{ver}'
    with open(FILENAME.format(dataset), 'rb') as f:
        return pickle.load(f)


def get_model(algo='knn_m', version=None):
    ver = f'_{version}' if version else ''
    model = f'{algo}{ver}'
    with open(FILENAME.format(model), 'rb') as f:
        return pickle.load(f)
