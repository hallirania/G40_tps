import http.client


def connect_to_google():
    path = ('/maps/geo?q=207N.+Defiance+St%2C+Archbold%2C+OH'
            '&output=json&oe=utf8')
    connection = http.client.HTTPConnection('maps.google.com')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    print(rawreply)


if __name__ == '__main__':
    connect_to_google()
    