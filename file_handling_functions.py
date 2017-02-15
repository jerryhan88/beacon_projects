import os
import pickle

def save_pklFile(path, _objects):
    with open(path, 'wb') as fp:
        pickle.dump(_objects, fp)

def load_pklFile(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)

def get_fnOnly(path):
    _, tail = os.path.split(path)
    return tail


def check_file_exist(path):
    return os.path.exists(path)


