class Client_Request(object):

    def __init__(self, query_string, top_k = 0):
        self.query_string = query_string
        self.top_k = top_k

class Server_Response(object):

    def __init__(self, time_to_process, ranked_list = []):
        self.ranked_list = ranked_list
        self.time_to_process = time_to_process
