from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import json
import argparse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Serving http host - default content')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Got this POST request: ')
        response.write(body)
        with open(filename, 'a+') as f:
            f.write(body.decode("utf-8"))
            f.write("\n")
        self.wfile.write(response.getvalue())


parser = argparse.ArgumentParser()
parser.add_argument("--logfile", default='received_posts.txt', help="filename of received posts ", type=str)
args = parser.parse_args()
filename = args.logfile

httpd = HTTPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
print("Serving on 127.0.0.1")
with open(filename,"w+") as f:
    f.write("Loggfile opened\n")
httpd.serve_forever()
