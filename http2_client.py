from ocr_struct import fruy_struct, FunctionArguments, Inputs, Outputs
from hyper import HTTPConnection
import ssl
import bson

def send_request(connection, url, data, method='POST', content_type='application/octet-stream'):
    """
    Send data to the Twisted HTTP/2 server.
    """
    connection.request(method, url, body=data, headers={'content-type': content_type})
    response = connection.get_response()
    return response.read()

def main():
    # Specify the server's hostname and port
    host = 'localhost'
    port = 8089

    # Set up the SSL context (assuming your server uses SSL)
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="certificates/cert.pem", keyfile="certificates/private.pem", password=None)

    # Create an HTTP/2 connection using hyper
    connection = HTTPConnection(host, port, secure=True, ssl_context=ssl_context)

    inputs = None
    with open("testdata/single_pdf.pdf", "rb") as fr:
        inputs = Inputs(pdf=fr.read())
    
    func_arguments = FunctionArguments(credentials={}, properties={})

    func_args_data = fruy_struct.serialize(func_arguments)
    inputs_data = fruy_struct.serialize(inputs)
    b_data = bson.dumps({'func_args': func_args_data, 'inputs': inputs_data})

    # Send data to the server and process the response
    response_data = send_request(connection, '/', data=b_data)

    outputs = fruy_struct.deserialize(response_data)

    print(outputs.ocr_json)
    print(outputs.raw_text)

if __name__ == "__main__":
    main()
