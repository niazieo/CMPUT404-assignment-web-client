#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Copyright 2023 Omar Niazie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split(' ')[1]
        #print("CODE:", code)
        return int(code)

    def get_headers(self,data):
        headers = data.split('\r\n\r\n')[0]
        #print("HEADERS:", headers)
        return headers

    def get_body(self, data):
        body = data.split('\r\n\r\n')
        #print("BODY:", body)
        if len(body) > 1:
            body = body[1]
            #print(body)
        else:
            body = body[0]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #print("URL:", url)
        host = urllib.parse.urlparse(url).hostname
        path = urllib.parse.urlparse(url).path or "/" 
        port = urllib.parse.urlparse(url).port or 80
        # test = "HOST: %s, PATH: %s, PORT: %d" %(host, path, port)
        # print(test)
        request = 'GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' %(path, host)
        #print("REQUEST:\n", request)
        self.connect(host, port)
        self.sendall(request)
        response = self.recvall(self.socket)
        #print("RESPONSE:\n", response)
        self.close()
        code = self.get_code(response)
        #print(code)
        body = self.get_body(response)
        #print(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        #print("URL:", url)
        host = urllib.parse.urlparse(url).hostname
        path = urllib.parse.urlparse(url).path or '/'
        port = urllib.parse.urlparse(url).port or 80
        # test = "HOST: %s, PATH: %s, PORT: %d" %(host, path, port)
        # print(test)
        # print("ARGS:", args)
        query = ''
        if args:
            # for key in args:
            #     args[key] = args[key].encode('utf-8')
            #     if '\r' and '\n' in args[key]:
            #         #print("ORIGINAL:", args[key])
            #         #args[key] = urllib.parse.urlencode(args[key])
            #         #args[key] = args[key].replace('\r', '')
            #         #print("NEW:", args[key])
            #         #args[key].join('\n')
            #     query += key + "=" + args[key] + "&"
            query = urllib.parse.urlencode(args)
            #print(query)
        #print("PATH+QUERY:", path + query)
        request = 'POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\nConnection: close\r\n\r\n' %(path+query, host, len(query))
        #print("REQUEST:\n", request)
        self.connect(host, port)
        self.sendall(request)
        response = self.recvall(self.socket)
        #print("RESPONSE:\n", response)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
