import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from views import getAllPosts


class JSONServer(HandleRequests):
    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                pass
                # return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = getAllPosts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

    def do_POST(self):
        pass

    def do_DELETE(self):
        pass

    def do_PUT(self):
        pass


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
