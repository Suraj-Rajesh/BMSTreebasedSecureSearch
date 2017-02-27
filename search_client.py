from bmssearch.communication_objects import Client_Request
from bmssearch.network_interface import send_object, receive_object
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

    def start_console(self):
        try:
            while True:
                # Get query data from user
                query_string = input("\nSearch: ")
                top_k = int(input("To  fetch the top-k results, enter value of k ( 0 to fetch all results): "))
                while top_k > 170: 
                    print("Server can handle a maximum of only top-170 results, try again...")
                    top_k = int(input("To  fetch the top-k results, enter value of k ( 0 to fetch all results): "))

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

        except KeyboardInterrupt:
            print("Client switching off...\n")

if __name__ == "__main__":
    search_client = Search_Client("127.0.0.1", 5000)
    search_client.start_console()
