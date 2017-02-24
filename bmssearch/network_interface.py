from pickle import loads, dumps

def send_object(sock, obj):
    """
    Use this to send objects across dataCenters
    """
    try:    
        data = dumps(obj)
        sock.send(data)
    except Exception as details:
        print(details)
        return None

def receive_object(sock):
    """
    Use this to receive objects across dataCenters
    """
    try:
        data = sock.recv(4096)
        obj = loads(data)
        return obj
    except Exception as details:
        print(details)
        return None
