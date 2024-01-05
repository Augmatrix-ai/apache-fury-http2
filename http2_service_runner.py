from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import endpoints
from abc import ABC, abstractmethod
from ocr_struct import fruy_struct, FunctionArguments, Inputs, Outputs
import bson

class ServiceRunner(Resource, ABC):
    isLeaf = True

    def render(self, request):
        # Read binary json to json
        data_json = bson.loads(request.content.read())
        func_args_data = data_json["func_args"]
        inputs_data = data_json["inputs"]

        # Deserialize func_args and inputs the structure
        func_args = fruy_struct.deserialize(func_args_data)
        inputs = fruy_struct.deserialize(inputs_data)

        # Get various data required to run the program
        self.properties = func_args.properties
        self.credentials = func_args.credentials
        inputs = inputs.__dict__

        outputs = self.run(**inputs)

        outputs = Outputs(**outputs)
        outputs_data = fruy_struct.serialize(outputs)

        # Write the byte data to the response
        request.write(outputs_data)

    @abstractmethod
    def run(self, request):
        assert False, "Method not implemented"

class ServerManager:
    def __init__(self, service_runner):
        self.service_runner = service_runner

    def start(self, host="localhost", port=8089, private_key="certificates/private.pem", cert_key="certificates/cert.pem"):
        site = server.Site(self.service_runner)
        if  private_key is not None and cert_key is not None:
            endpoint_spec = f"ssl:port={port}:privateKey={private_key}:certKey={cert_key}:interface={host}"
        else:
            endpoint_spec = f"ssl:port={port}:interface={host}"
        
        server_endpoint = endpoints.serverFromString(reactor, endpoint_spec)
        server_endpoint.listen(site)
        reactor.run()