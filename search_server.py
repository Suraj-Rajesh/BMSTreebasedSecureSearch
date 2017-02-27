import threading
import socket
from time import time
from random import randint
from operator import itemgetter
from math import sqrt
from copy import deepcopy

from hashlib import sha256

from bmssearch.crypto import aes_decrypt
from bmssearch.network_interface import send_object, receive_object
from bmssearch.communication_objects import Server_Response
from bmssearch.helpers.operations import load_object, matrix_multiplication, vsm_hash_to_vsm
from bmssearch.helpers.text_processor import stem_text

class SearchServer(object):

    def __init__(self, port = 5000, is_cached = False):
        self.port = port
        self.cached = is_cached

        # Load key, salt and secret
        self.aes_key = load_object("index/aes_key.pkl")
        self.salt = load_object("index/salt.pkl")
        self.secret = load_object("index/secret.pkl")

        # Load matrices
        self.m1i = load_object("index/m1i.pkl")
        self.m2i = load_object("index/m2i.pkl")

        # Load encrypted token map & encrypted search index(BMS Tree)
        self.encrypted_token_map = load_object("index/encrypted_token_map.pkl")
        self.encrypted_bmst = load_object("index/encrypted_bmst.pkl")

        # Initialize server socket to handle incoming connections
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind(("0.0.0.0", self.port))
        self.serverSock.listen(128)

    def start(self):
        # Start listening for incoming requests
        print("\nServer ready...\n")
        while 1:
            connection, address = self.serverSock.accept()
            threading.Thread(target=self.requestHandler, args=(connection, address)).start()

    def requestHandler(self, server_socket, address):
        # Receive query & search parameters from the client
        client_query_object = receive_object(server_socket)

        # Info
        print("Received request for: " + client_query_object.query_string + "\n")

        # Start timer
        start_time = time()

        query = client_query_object.query_string
        top_k = client_query_object.top_k

        # Server can handle a max of 170 top-k for now
        if top_k == 0 or top_k > 170:
            top_k = 170

        # Prepare the hashed query
        stemmed_query = stem_text(query)
        query_terms = list(set(stemmed_query.split()))
        hashed_query_terms = [sha256(self.salt.encode() + query.encode()).hexdigest() for query in query_terms]

        # Prepare hashed index for query indices
        query_map = dict()

        for query in hashed_query_terms:
            if query in self.encrypted_token_map:
                # Create query map: index:idf
                query_map[self.encrypted_token_map[query][0]] = self.encrypted_token_map[query][1]

        # Create normalized idf for query map
        normalization = sqrt(sum([ pow(idf, 2) for idf in query_map.values()]))
        query_map = { index : idf/normalization for index, idf in query_map.items() }

        # Generate q1 and q2
        q1 = deepcopy(query_map)
        q2 = deepcopy(query_map)

        for index in query_map.keys():
            if self.secret[index] == 0:
                # Split randomly as long as the sum is same
                q1[index] = query_map[index]/(randint(2,4))
                q2[index] = query_map[index] - q1[index]

        # Encrypt query vectors
        n = len(self.encrypted_token_map)

        m1iq1 = matrix_multiplication(self.m1i, vsm_hash_to_vsm(n, q1))
        m2iq2 = matrix_multiplication(self.m2i, vsm_hash_to_vsm(n, q2))

        ranked_result = list()

        # Search in encrypted bmst & get a list of matching file nodes
        file_nodes = list()
        file_nodes = self.encrypted_bmst.search([m1iq1, m2iq2], file_nodes, top_k)

        # results_map: {similarity score: filename}
        results_map = { (aes_decrypt(matched_entry[0], self.aes_key)).decode("utf-8") :  matched_entry[1] for matched_entry in file_nodes }
        print(results_map)

        # Sort by similarity score
        ranked_result = sorted(results_map.items(), key = itemgetter(1), reverse = True)
        ranked_result = [result[0] for result in ranked_result]

        # Note end time
        end_time = time()

        # Create response to client
        response = Server_Response(float("{0:.4f}".format(end_time - start_time)), ranked_result)

        # Send response back to the client
        send_object(server_socket, response)

        # Close socket
        server_socket.close()

if __name__ == "__main__":
    # Start the server
    try:
        encrypted_search_server = SearchServer()
        encrypted_search_server.start()
    except KeyboardInterrupt:
        encrypted_search_server.serverSock.close()
        print("\nServer shutting down...\n")
