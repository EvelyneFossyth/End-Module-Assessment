from http.server import BaseHTTPRequestHandler


# Server program
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Receive the serialized dictionary and encrypted text file
        content_len = int(self.headers.get('Content-Length'))
        self.rfile.read(content_len)
        with open('received_text_file.txt', 'wb') as file:
            file.write(self.rfile.read(int(self.headers['Content-Length'])))

        # Deserialize the dictionary using the specified format
        input("Enter the pickling format (binary, JSON, or XML): ")
