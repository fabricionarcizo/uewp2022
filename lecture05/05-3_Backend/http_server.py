#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2022 Fabricio Batista Narcizo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
A very simple HTTP server developing in Python for logging HTTP requests and
storing user"s data in a SQLite database.

Usage::
    ./http_server.py [<port>]
"""

from argparse import ArgumentParser, SUPPRESS

import cgi
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer

from html_utils import HTML_Utils
from db.sqlite_db import create_students_table
from db.sqlite_db import delete_student_record
from db.sqlite_db import insert_student_record


class WebServer(BaseHTTPRequestHandler):
    """WebServer is a class to manage a simple HTTP server and web data from an SQLite database."""

    def __set_response(self, encoding: str="text/html"):
        """Create the response header to the headers buffer and log the response
        code, and sends a MIME header to the headers buffer.

        Args:
            encoding (str, optional): The enconding string of the request web 
                file. Defaults to "text/html".
        """
        self.send_response(200)
        self.send_header("Content-type", encoding)
        self.end_headers()

    def do_GET(self):
        """This method serves the `GET` request type. It receives a request and 
        map it to a local file by interpreting the request as a path relative to
        the current working directory."""

        # Log a message with severity 'INFO' on the root logger.
        logging.info(
            f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")

        # Handle GET requests to the root path.
        if self.path == "/":
            html = HTML_Utils.show_db_records()
            self.__set_response()
            self.wfile.write(bytes(html, "utf-8"))

        # Handle GET requests to the style sheet file.
        elif self.path == "/styles/main.css":
            css = HTML_Utils.read_template("styles/main.css")
            self.__set_response("text/css")
            self.wfile.write(bytes(css, "utf-8"))

    def do_POST(self):
        """This method serves the `POST` request type, only allowed for CGI
        scripts. Error 501, `Can only POST to CGI scripts`, is output when
        trying to POST to a non-CGI url."""

        # Log a message with severity 'INFO' on the root logger.
        logging.info(
            f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")

        # Get the main content-type and a dictionary of options.
        key, pdict = cgi.parse_header(self.headers.get("content-type"))
        pdict["boundary"] = bytes(pdict["boundary"], "utf-8")

        # Hint: It is mandatory to define the following `enctype` attribute
        # in your HTML form: enctype="multipart/form-data".
        if key == "multipart/form-data":

            # Get the students fields from your HTML form.
            fields = cgi.parse_multipart(self.rfile, pdict)

            # The result HTML data.
            html = ""

            # Handle POST requests to the `/insert` path.
            if self.path == "/insert":

                # Get the students fields data.
                name = email = secret = ""
                try:
                    name = fields.get("name")[0]
                    email = fields.get("email")[0]
                    secret = fields.get("secret")[0]
                except:
                    logging.error(
                        f"You didn't submit a mandatory field.\n")

                # It is mandatory to send the secret password to insert a new
                # record in the SQLite dataset.
                if secret == "123":
                    insert_student_record(name, email)
                    html = HTML_Utils.read_template("html/insert.html")
                else:
                    html = HTML_Utils.read_template("html/error.html")

            # Handle POST requests to the `/delete` path.
            elif self.path == "/delete":

                # Get the students fields data.
                uid = secret = ""
                try:
                    uid = fields.get("uid")[0]
                    secret = fields.get("secret")[0]
                except:
                    logging.error(
                        f"You didn't submit a mandatory field.\n")

                # It is mandatory to send the secret password to insert a new
                # record in the SQLite dataset.
                if secret == "123":
                    try:
                        delete_student_record(uid)
                        html = HTML_Utils.read_template("html/delete.html")
                    except:
                        html = HTML_Utils.read_template("html/error.html")
                else:
                    html = HTML_Utils.read_template("html/error.html")

            # Check if there is a valid HTML result.
            if html != "":
                self.__set_response()
                self.wfile.write(bytes(html, "utf-8"))


def run(server_class: HTTPServer=HTTPServer,
        handler_class: BaseHTTPRequestHandler=WebServer, port: int=8080):
    """Create and listen at the HTTP socket, dispatching the requests to a 
    handler.

    Args:
        server_class (HTTPServer, optional): It uses the Internet TCP protocol,
            which provides for continuous streams of data between the client and
            server. Default to `HTTPServer`.
        handler_class (BaseHTTPRequestHandler, optional): A personalized object
            used to handle the HTTP requests that arrive at the server. Default
            to `WebServer`.
        port (int, optional): The TCP/IP port used to receive HTTP requests. 
            Default to `8080`.
    """

    # Create `students` when runs the script for the first time.
    create_students_table()

    # Define the basic configuration for the logging system.
    logging.basicConfig(level=logging.INFO)

    # Start the web server.
    server_address = ("localhost", port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    # Stop the web server.
    httpd.server_close()
    logging.info("Stopping httpd...\n")


def build_argparser() -> ArgumentParser():
    """Argument builder for construction via terminal.

    Returns:
        ArgumentParser: Constructed argumentparser.
    """
    parser = ArgumentParser(add_help=False)
    arg_group = parser.add_argument_group("Options")
    arg_group.add_argument(
        "-h", "--help",
        action="help",
        default=SUPPRESS,
        help="Show this help message and exit.")

    arg_group.add_argument(
        "-p", "--port",
        default=8080,
        help="Optional. The web server port.",
        type=int)

    return parser


if __name__ == "__main__":
    args = build_argparser().parse_args()
    run(port=args.port)
