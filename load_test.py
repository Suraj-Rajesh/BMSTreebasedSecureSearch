from pps.communication_objects import Client_Request
from pps.network_interface import send_object, receive_object
import socket

class Search_Client(object):

    def __init__(self, server_ip, server_port):
        self.server_connection_parameters = (server_ip, int(server_port))

    def present_response(self, server_response):
        print("\n")
        for filename in server_response.ranked_list:
            print(filename)
        print("\nNumber of matching files: " + str(len(server_response.ranked_list)))
        print("\nServer query processing time: " + str(server_response.time_to_process) + " s")

    def start_load(self, iterations):
        try:
            for i in range(iterations):
                # Get query data from user
                query_string = "bengaluru america library ocean atlantic create surprise california search research sun solar thesis atlantic pacific asia china india bangalore machine configuration test implement medicine machine plant time minutes seconds milli hours"

                top_k = 0

                # Format query 
                request = Client_Request(query_string, top_k)

                # Create socket
                client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_sock.connect(self.server_connection_parameters)

                # Send query to server
                send_object(client_sock, request)

                # Receive response from server
                server_response = receive_object(client_sock)
                client_sock.close()

                # Present response to the user
                self.present_response(server_response)
                print(i)

        except KeyboardInterrupt:
            print("Client switching off...\n")

if __name__ == "__main__":
    search_client = Search_Client("127.0.0.1", 5000)
    search_client.start_load(1000)
