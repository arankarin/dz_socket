import socket


end_of_stream = '\r\n\r\n'


def method_checking(status):
    status_codes = {'100': 'CONTINUE', '101': 'SWITCHING_PROTOCOLS', '102': 'PROCESSING', '103': 'EARLY_HINTS',
                    '200': 'OK', '201': 'CREATED', '202': 'ACCEPTED', '203': 'NON_AUTHORITATIVE_INFORMATION',
                    '204': 'NO_CONTENT','205': 'RESET_CONTENT', '206': 'PARTIAL_CONTENT', '207': 'MULTI_STATUS',
                    '208': 'ALREADY_REPORTED', '226': 'IM_USED',
                    '300': 'MULTIPLE_CHOICES', '301': 'MOVED_PERMANENTLY', '302': 'FOUND',
                    '303': 'SEE_OTHER', '304': 'NOT_MODIFIED', '305': 'USE_PROXY', '307': 'TEMPORARY_REDIRECT',
                    '308': 'PERMANENT_REDIRECT',
                    '400': 'BAD_REQUEST', '401': 'UNAUTHORIZED', '402': 'PAYMENT_REQUIRED', '403': 'FORBIDDEN',
                    '404': 'NOT_FOUND', '405': 'METHOD_NOT_ALLOWED', '406': 'NOT_ACCEPTABLE',
                    '407': 'PROXY_AUTHENTICATION_REQUIRED', '408': 'REQUEST_TIMEOUT', '409': 'CONFLICT', '410': 'GONE',
                    '411': 'LENGTH_REQUIRED', '412': 'PRECONDITION_FAILED', '413': 'REQUEST_ENTITY_TOO_LARGE',
                    '414': 'REQUEST_URI_TOO_LONG', '415': 'UNSUPPORTED_MEDIA_TYPE',
                    '416': 'REQUESTED_RANGE_NOT_SATISFIABLE', '417': 'EXPECTATION_FAILED', '418': 'IM_A_TEAPOT',
                    '421': 'MISDIRECTED_REQUEST', '422': 'UNPROCESSABLE_ENTITY', '423': 'LOCKED',
                    '424': 'FAILED_DEPENDENCY', '425': 'TOO_EARLY', '426': 'UPGRADE_REQUIRED',
                    '428': 'PRECONDITION_REQUIRED', '429': 'TOO_MANY_REQUESTS', '431': 'REQUEST_HEADER_FIELDS_TOO_LARGE',
                    '451': 'UNAVAILABLE_FOR_LEGAL_REASONS',
                    '500': 'INTERNAL_SERVER_ERROR', '501': 'NOT_IMPLEMENTED', '502': 'BAD_GATEWAY',
                    '503': 'SERVICE_UNAVAILABLE', '504': 'GATEWAY_TIMEOUT', '505': 'HTTP_VERSION_NOT_SUPPORTED',
                    '506': 'VARIANT_ALSO_NEGOTIATES', '507': 'INSUFFICIENT_STORAGE', '508': 'LOOP_DETECTED',
                    '510': 'NOT_EXTENDED', '511': 'NETWORK_AUTHENTICATION_REQUIRED'}

    if status in status_codes.keys():
        return status, status_codes[status]
    else:
        status = '200'
        status_ok = 'OK'
        return status, status_ok

def handle_client(connection):
    client_data = ''
    with connection:
        while True:
            data = connection.recv(1024)
            print("Received:", data)
            if not data:
                break
            client_data += data.decode()
            print(f"client_data = {client_data}")
            if end_of_stream in client_data:
                break
        client_data = client_data.split('\r\n')
        status_all = client_data[0].split(' ')
        nunber_slice = status_all[1].find('=')
        status = status_all[1][nunber_slice + 1:]
        print(f"client_data = {client_data}")
        nunber_request_method = client_data[0].find('/')
        request_method = client_data[0][:nunber_request_method]
        print(f"request_method = {request_method}")
        print(f"status = {status}")
        res, res2 = method_checking(status)
        request_source_all = client_data[4].split(":")
        request_source = (request_source_all[1], int(request_source_all[2]))
        headers = '\r\n'.join(client_data[1:])
        response_to_client = f'HTTP/1.1 {res} {res2} {headers}'
        print(f"response_to_client = {response_to_client}")
        response_info = f'Request Method: {request_method}\r\nRequest Source: {request_source}\r\n' \
                        f'Response Status: {res} {res2}'
        print('Sending to the client:')
        print(response_to_client)
        print(response_info)

        connection.send(response_to_client.encode() + response_info.encode())


with socket.socket() as serverSocket:
    serverSocket.bind(("127.0.0.1", 40406))
    serverSocket.listen()

    while True:
        (clientConnection, clientAddress) = serverSocket.accept()
        handle_client(clientConnection, clientAddress)
        print(f"Sent data to {clientAddress}\n")