#!C:\Python27\python.exe -u

import BaseHTTPServer
import CGIHTTPServer
httpd = BaseHTTPServer.HTTPServer(\
    ('localhost', 88), \
CGIHTTPServer.CGIHTTPRequestHandler)
###  here some code to say, hey please execute python script on the webserver... ;-)
httpd.serve_forever()