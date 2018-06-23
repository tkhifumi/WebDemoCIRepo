#!/usr/bin/env python

"""Simple HTTP server for Robot Framework web testing demo.

Usage:  server.py [port]

This server serves HTML pages under `html` directory. Server is started simply
by running this script from the command line or double-clicking it in a file
manager. In the former case the server can be shut down with Ctrl-C and in the
latter case by closing the opened window.

By default the server uses port 7272, but a custom port can be given as
an argument from the command line.
"""

from __future__ import print_function

from os import chdir
from os.path import abspath, dirname, join
import socket
try:
    from SocketServer import ThreadingMixIn
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer


ROOT = join(dirname(abspath(__file__)), 'html')
PORT = 7272


class DemoRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            except BrokenPipeError:
                print('Detect Remote disconnect')
            finally:
                f.close()

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                    HTTPStatus.NOT_IMPLEMENTED,
                    "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            if not self.wfile.closed:
                self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return

class DemoServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def __init__(self, port=PORT):
        HTTPServer.__init__(self, ('localhost', int(port)),
                            DemoRequestHandler)

    def serve(self, directory=ROOT):
        chdir(directory)
        print('Demo server starting on port %d.' % self.server_address[1])
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
        print('Demo server stopped.')


if __name__ == '__main__':
    import sys
    try:
        server = DemoServer(*sys.argv[1:])
    except (TypeError, ValueError):
        print(__doc__)
    else:
        server.serve()
