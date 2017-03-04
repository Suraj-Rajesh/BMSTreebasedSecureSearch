import sys

import numpy as np
from pickle import load, dump

def generate_orthonormal_matrix(dimension):
     random_state = np.random
     H = np.eye(dimension)
     D = np.ones((dimension,))

     for n in range(1, dimension):
         print(str(n) + " of " + str(dimension))
         x = random_state.normal(size=(dimension-n+1,))
         D[n-1] = np.sign(x[0])
         x[0] -= D[n-1]*np.sqrt((x*x).sum())

         # Householder transformation
         Hx = (np.eye(dimension-n+1) - 2.*np.outer(x, x)/(x*x).sum())
         mat = np.eye(dimension)
         mat[n-1:, n-1:] = Hx
         H = np.dot(H, mat)

     # Fix the last sign such that the determinant is 1
     D[-1] = (-1)**(1-(dimension % 2))*D.prod()
     # Equivalent to np.dot(np.diag(D), H) but faster, apparently
     H = (D*H.T).T

     # Check if generated matrix is well defined
     if np.linalg.cond(H) < 1/sys.float_info.epsilon:
        print("\nGenerated matrix is well-defined...\n")
     else:
         print("\nMatrix not well-defined. Re-generate matrix...\n")

     return H

def generate_random_invertible_matrix(n):
#    return np.triu(np.random.random_integers(range_lower, range_upper, (n, n)))
#    return generate_orthonormal_matrix(n)
    matrix = np.random.random_integers(1, 2, (n, n))

    # Check condition of matrix
    if np.linalg.cond(matrix) < 1/sys.float_info.epsilon:
        print("\nGenerated matrix is well defined...\n")
    else:
        print("\nMatrix not well-defined. Re-generate matrix...\n")

    return matrix

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
