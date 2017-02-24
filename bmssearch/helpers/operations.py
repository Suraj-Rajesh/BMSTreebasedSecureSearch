import numpy as np
from pickle import load, dump

def generate_random_invertible_matrix(n, range_lower, range_upper):
    return np.triu(np.random.random_integers(range_lower, range_upper, (n, n)))

def get_inverse(matrix):
    return np.linalg.inv(matrix)

def get_transpose(matrix):
    return matrix.T

def matrix_multiplication(matrix_1, matrix_2):
    return np.dot(matrix_1, matrix_2)

def vsm_hash_to_vsm(n, vsm_hash):
    vsm = [0] * n

    for index in vsm_hash:
        vsm[index] = vsm_hash[index]

    return vsm

def save_object(filename, obj):
    with open(filename, "wb") as output:
        dump(obj, output, -1)

def load_object(object_file):
    with open(object_file, "rb") as inpt:
        index = load(inpt, encoding="latin1")
    return index
