import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import create_user, login_user, getAllPosts


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                pass
                # return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = getAllPosts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

    def do_PUT(self):
        """Handle PUT requests from a client"""

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

    def do_POST(self):
        """Handle POST requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            new_user = create_user(request_body)
            return self.response(
                json.dumps(new_user), status.HTTP_201_SUCCESS_CREATED.value
            )

        if url["requested_resource"] == "login":
            currentUser = login_user(request_body)
            currentUser = json.loads(currentUser)
            if currentUser["valid"] is True:
                return self.response(
                    json.dumps(currentUser), status.HTTP_200_SUCCESS.value
                )
            else:
                return self.response(
                    json.dumps(currentUser),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
