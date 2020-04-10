from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from gesture import Gesture

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2','/')

# Create server
server = SimpleXMLRPCServer(("localhost", 9090),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

def predict(filename):
    gesture = Gesture.from_abs_file(filename)[0]
    return gesture.predict()

server.register_function(predict, 'predict')
server.serve_forever()
