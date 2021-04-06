import pickle

FILENAME = 'recsys/{}.pkl'


def get_data(data='dataset', normalized=False):
    prefix = 'n_' if normalized else ''
    dataset = f'{prefix}{data}'
    with open(FILENAME.format(dataset), 'rb') as f:
        return pickle.load(f)


def get_model(algo='knn_m', version=1):
    model = f'{algo}_{version}'
    with open(FILENAME.format(model), 'rb') as f:
        return pickle.load(f)
