import pickle
import json
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Receive the serialized dictionary and encrypted text file
        content_len = int(self.headers.get('Content-Length'))
        serialized_dict = self.rfile.read(content_len)
        with open('received_text_file.txt', 'wb') as f:
            f.write(self.rfile.read(int(self.headers['Content-Length'])))

        # Deserialize the dictionary using the specified format
        pickling_format = input("Enter the pickling format (binary, JSON, or XML): ")
        if pickling_format == "binary":
            my_dict = pickle.loads(serialized_dict)
        elif pickling_format == "JSON":
            my_dict = json.loads(serialized_dict)
        elif pickling_format == "XML":
            root = ET.fromstring(serialized_dict)
            my_dict = {}
            for child in root:
                my_dict[child.tag] = child.text

        # Print the dictionary and contents of the text file
        print(my_dict)
        with open('received_text_file.txt', 'r') as f:
            print(f.read())

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Received')


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 8080...')
    httpd.serve_forever()
