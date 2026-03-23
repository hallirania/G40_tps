import socket


def connect_to_google():
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))
    request = (
        'GET /maps/geo?q=207N.+Defiance+St%2C+Archbold%2C+OH'
        '&output=json&oe=utf8&sensor=false HTTP/1.1\r\n'
        'Host: maps.google.com:80\r\n'
        'User-Agent: search4.py\r\n'
        'Connection: close\r\n'
        '\r\n'
    )
    sock.sendall(request.encode('ascii'))

    rawreply = sock.recv(4096)
    print(rawreply.decode(errors='ignore'))


if __name__ == '__main__':
    connect_to_google()