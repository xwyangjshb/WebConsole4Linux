# -*- coding:utf8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from os import path

curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
            ('.html', 'text/html'),
            ('.htm', 'text/html'),
            ('.js', 'application/javascript'),
            ('.css', 'text/css'),
            ('.json', 'application/json'),
            ('.png', 'image/png'),
            ('.jpg', 'image/jpeg'),
            ('.gif', 'image/gif'),
            ('.txt', 'text/plain'),
            ('.avi', 'video/x-msvideo'),
        ]

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = urlparse(self.path).path
        file_query = urlparse(self.path).query
        print(file_path)
        print(file_query)
        # print(self.client_address)
        send_reply = False
        if file_path == "/":
            file_path += "index.html"

            filename, fileext = path.splitext(file_path)
            for m in mimedic:
                if m[0] == fileext:
                    mimetype = m[1]
                    send_reply = True

            if send_reply == True:
                try:
                    with open(path.realpath(curdir + sep + file_path), 'rb') as f:
                        content = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', mimetype)
                        self.end_headers()
                        self.wfile.write(content)
                except IOError:
                    self.send_error(404, 'File Not Found: %s' % self.path)
        elif file_path == "/cgi-bin/format.cgi":
            self.send_response(200)
            forms = {}
            for item in file_query.split("&"):
                forms.update({item.split("=")[0]: item.split("=")[1]})
                print(forms)

def run(server_class=HTTPServer, handler_class=HTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("server start success")
    httpd.serve_forever()

if __name__ == "__main__":
    run()