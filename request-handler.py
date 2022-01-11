from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_animals, get_single_animal, create_animal


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self):
        # /animals/1 (animals, 1)
        split_path = self.path.split('/') # ['', 'animals', 1]
        resource = split_path[1]
        id = None
        try:
            id = int(split_path[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)


    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        print(self.path)
        
        resource, id = self.parse_url()

        if 'animals' == resource:
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals()
        else:
            response = []

        self.wfile.write(f"{response}".encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        request = json.loads(post_body)
        new_animal = None
        resource, _ = self.parse_url()

        if 'animals' == resource:
            new_animal = create_animal(request)

        self.wfile.write(f'{new_animal}'.encode())

    def do_PUT(self):
        self.do_POST()

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()