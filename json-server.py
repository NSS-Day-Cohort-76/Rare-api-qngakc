import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for orders"""
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()