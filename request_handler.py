import json
from urllib.parse import urlparse, parse_qs

from views import get_all_snakes, get_all_species, get_all_owners, get_single_snake, get_single_owner, get_single_species, get_snakes_by_species, create_snake

from http.server import BaseHTTPRequestHandler, HTTPServer


class HandleRequests(BaseHTTPRequestHandler):

    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """Handles GET requests to the server
        """

        response = {}

        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "snakes":
                if id is not None:
                    response = get_single_snake(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(405)

                else:
                    self._set_headers(200)
                    response = get_all_snakes()
            elif resource == "species":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_species(id)
                else:
                    self._set_headers(200)
                    response = get_all_species()
            elif resource == "owners":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_owner(id)
                else:
                    self._set_headers(200)
                    response = get_all_owners()

            else:
                self._set_headers(404)
                response = []

        else:
            self._set_headers(200)

            (resource, query) = parsed

            if query.get('species_id') and resource == 'snakes':
                response = get_snakes_by_species(query['species_id'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_snake = None

        if resource == "snakes":
            if "name" in post_body and "owner_id" in post_body and "species_id" and "gender" and "color" in post_body:
                self._set_headers(201)
                new_snake = create_snake(post_body)
                self.wfile.write(json.dumps(new_snake))
            else:
                self._set_headers(400)

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self.do_PUT()

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

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


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
