from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_animals, get_single_animal, create_animal
from views.animal_requests import delete_animal, get_animals_by_search, update_animal
from views.customer_requests import (
    get_all_customers, get_customer_by_email, get_customers_by_name, get_single_customer)
from views.employee_requests import get_all_employees, get_single_employee
from views.location_requests import get_all_locations

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        # /animals
        # /animals/1 (animals, 1)
        # /customers?email=jenna@solis.com
        path_params = self.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]  # email=jenna@solis.com
            resource = resource.split('?')[0]  # customer
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
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
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)

        print(self.path)

        parsed = self.parse_url()
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == 'animals':
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_locations()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
        if len(parsed) == 3:
            (resource, key, value) = parsed

            if key == 'email' and resource == 'customers':
                response = get_customer_by_email(value)
            elif key == "name" and resource == "customers":
                response = get_customers_by_name(value)
            elif key == "search" and resource == 'animals':
                response = get_animals_by_search(value)

        self.wfile.write(response.encode())

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
        """Handles PUT requests to the server"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        request = json.loads(post_body)

        resource, id = self.parse_url()
        is_succesful = False
        if resource == 'animals':
            is_succesful = update_animal(id, request)

        if is_succesful:
            self._set_headers(204)
        else:
            self._set_headers(404)

    def do_DELETE(self):
        """Handle DELETE Requests"""
        resource, id = self.parse_url()
        was_updated = False
        if resource == 'animals':
            was_updated = delete_animal(id)

        if was_updated:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write(''.encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
