from os import listdir
from random import randint
from uuid import uuid4
from hashlib import sha256
from math import log
from collections import defaultdict
from copy import deepcopy

from textblob import TextBlob as tb

from bmssearch.bmst import Node
from bmssearch.crypto import generate_aes_key, aes_encrypt, aes_decrypt
from bmssearch.helpers.tf_idf_generator import tf, n_containing, idf, tfidf
from bmssearch.helpers.operations import load_object, save_object, generate_random_invertible_matrix, get_transpose, get_inverse, matrix_multiplication, vsm_hash_to_vsm

token_map = dict()
corpus_textblobs = dict()
secret = list()

# Keys and salt
salt = uuid4().hex
aes_key = 0

# Term count in corpus
n = 0

# Encryption matrices
m1t = 0
m2t = 0
m1i = 0
m2i = 0

def load_documents(directory):
    from bmssearch.helpers.text_processor import doc_to_text
    global corpus_textblobs

    files = listdir(directory)

    for filename in files:
        text = doc_to_text(directory + "/" + filename)
        textblob = tb(text)
        corpus_textblobs[filename] = textblob

def generate_token_map_and_secret(index_directory):
    global token_map
    global corpus_textblobs
    global n
    global secret

    index = 0

    for file_content in corpus_textblobs.values():
        for word in file_content.words:
            if word not in token_map:
                token_map[word] = [index, idf(word, corpus_textblobs)]
                index += 1

    n = len(token_map)
    save_object(index_directory + "/n.pkl", n)

    # Hash token map into a new encrypted token map
    encrypted_token_map = { sha256(salt.encode() + token.encode()).hexdigest() : metadata for token, metadata in token_map.items()}

    # Generate secret
    secret = [randint(0, 1) for i in range(n)]

    save_object(index_directory + "/token_map.pkl", token_map)
    save_object(index_directory + "/encrypted_token_map.pkl", encrypted_token_map)
    save_object(index_directory + "/secret.pkl", secret)

def create_vsm_hash(vsm_hash_1, vsm_hash_2, vsm_hash_3, vsm_hash_4):
    
    # Convert vsm_hash dict's passed to defaultdict with lamdba key defaulting to -1 to handle KeyError
    vsm_hash_1_dd = defaultdict(lambda: -1, vsm_hash_1)
    vsm_hash_2_dd = defaultdict(lambda: -1, vsm_hash_2)
    vsm_hash_3_dd = defaultdict(lambda: -1, vsm_hash_3)
    vsm_hash_4_dd = defaultdict(lambda: -1, vsm_hash_4)

    return { index : max(vsm_hash_1_dd[index], vsm_hash_2_dd[index], vsm_hash_3_dd[index], vsm_hash_4_dd[index]) for index in list(set(vsm_hash_1) | set(vsm_hash_2) | set(vsm_hash_3) | set(vsm_hash_4))}

def encrypt_vsm(vsm_hash):
    global n
    global secret
    global m1t
    global m2t

    encrypted_vsm_hash_1 = deepcopy(vsm_hash)
    encrypted_vsm_hash_2 = deepcopy(vsm_hash)

    for index in range(len(secret)):
        if secret[index] == 1:
            if index in vsm_hash:
                # Split randomly such that their addition equals the original value
                encrypted_vsm_hash_1[index] = vsm_hash[index]/(randint(2, 6))
                encrypted_vsm_hash_2[index] = vsm_hash[index] - encrypted_vsm_hash_1[index]

    encrypted_vsm_hash_1 = matrix_multiplication(m1t, vsm_hash_to_vsm(n, encrypted_vsm_hash_1))
    encrypted_vsm_hash_2 = matrix_multiplication(m2t, vsm_hash_to_vsm(n, encrypted_vsm_hash_2))

    return (encrypted_vsm_hash_1, encrypted_vsm_hash_2)


def build_bmst(corpus_textblobs, index_directory):
    global n
    global salt
    global aes_key

    try:
        current_processing_list = list()

        # For each file to be indexed
        for filename, textblob in corpus_textblobs.items():
            # Calculate score of all words in the textblob corresponding to that file
            word_score_index = {word: tfidf(word, textblob, corpus_textblobs) for word in textblob.words}
           
            vsm_hash = dict()

            for word in word_score_index:
                vsm_hash[token_map[word][0]] = word_score_index[word] 

            # Encrypt vsm hash of file node, create file node & add to processing list
            (encrypted_vsm_hash_1, encrypted_vsm_hash_2) = encrypt_vsm(vsm_hash)

            file_node = Node(vsm_hash = vsm_hash, filename = aes_encrypt(filename, aes_key), encrypted_vsm_hash_1 = encrypted_vsm_hash_1, encrypted_vsm_hash_2 = encrypted_vsm_hash_2)       
            current_processing_list.append(file_node)
    
        # Generating internal nodes, until we reach the root node
        while len(current_processing_list) != 1:

            new_processing_list = list()

            for i in range(0, len(current_processing_list), 4):
                new_vsm_hash = create_vsm_hash(current_processing_list[i].vsm_hash, current_processing_list[i + 1].vsm_hash, current_processing_list[i + 2].vsm_hash, current_processing_list[i + 3].vsm_hash)
                
                # Encrypt VSM hashes
                (encrypted_vsm_hash_1, encrypted_vsm_hash_2) = encrypt_vsm(new_vsm_hash)
                
                # Clear VSM values of child nodes & create children's list  
                index = i
                children = list()

                for j in range(4):
                    current_processing_list[index].vsm_hash = None
                    children.append(current_processing_list[index])
                    index += 1

                new_internal_node = Node(vsm_hash = new_vsm_hash, encrypted_vsm_hash_1 = encrypted_vsm_hash_1, encrypted_vsm_hash_2 = encrypted_vsm_hash_2, children = children)

                new_processing_list.append(new_internal_node)
            
            current_processing_list = new_processing_list

        root_node = current_processing_list[0]
        root_node.vsm_hash = None

        save_object(index_directory + "/encrypted_bmst.pkl", root_node)

    except KeyboardInterrupt:
        pass

def start_index_generation(prepared_documents_path, index_directory):
    global corpus_textblobs
    global salt
    global aes_key
    global m1t
    global m2t
    global m1i
    global m2i

    # STAGE 1

    print("\nSTAGE 1: \n\nGenerating textblobs...\n")

    load_documents(prepared_documents_path)

    print("Preparing index...\n")

    save_object(index_directory + "/salt.pkl", salt)

    aes_key = generate_aes_key()
    save_object(index_directory + "/aes_key.pkl", aes_key)

    generate_token_map_and_secret(index_directory)

    # STAGE 2
    # Create random invertible matrices and store Mt and Mi
    # This is being done as matrix generation from python prompt was much faster than generating it here in the function(esp. for      large matrices)
    user_input = input("\nEntering STAGE 2 of index generation:\n\n1. Go to bmssearch/helpers directory\n2. Load python3 prompt\n3. Import: from operations import *\nn = load_object('../../index/n.pkl')\n4. Create:\n\tm1 = generate_orthonormal_matrix(n)\n\tm2 = generate_orthonormal_matrix(n)\nSave matrices:\n\tsave_object('../../index/m1.pkl', m1)\n\tsave_object('../../index/m2.pkl', m2)\nType 'y' once done\n\nEnter here: ")

    if user_input == "y":
        m1 = load_object(index_directory + "/m1.pkl")
        m2 = load_object(index_directory + "/m2.pkl")

        # Get transpose of matrices
        m1t = get_transpose(m1)
        m2t = get_transpose(m2)

        # Get matrix inverses
        m1i = get_inverse(m1)
        m2i = get_inverse(m2)

        # Save matrices
        save_object(index_directory + "/m1t.pkl", m1t)
        save_object(index_directory + "/m2t.pkl", m2t)
        save_object(index_directory + "/m1i.pkl", m1i)
        save_object(index_directory + "/m2i.pkl", m2i)

        build_bmst(corpus_textblobs, index_directory)

    else:
        print("\nError procesisng with STAGE 2 of index generation. Index generation terminating...\n")
