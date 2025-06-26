import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import (
    create_user,
    login_user,
    getAllPosts,
    get_all_tags,
    create_tag,
    update_tag,
    retrieve_myposts,
    getSinglePost,
    create_post,
    create_category,
    get_all_categories,
    display_comments,
    create_comment,
    delete_category,
    get_all_users,
    delete_post,
    update_post,
    delete_tag,
    delete_comment,
    update_comment,
    update_category,
    get_all_reactions,
    create_reaction,
    delete_reaction,
    create_subscription,
    get_all_subscriptions,
    delete_subscription,
    get_single_user,
    add_post_reaction,
    update_user_status
)



class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = getSinglePost(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = getAllPosts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
       
        if url["requested_resource"] == "tags":
            if url["pk"] != 0:
                pass
            response_body = get_all_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "myposts":
            if url["pk"] != 0:
                response_body = retrieve_myposts(pk, url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
        
        if url["requested_resource"] == "categories":
            if url["pk"] != 0:
                pass
            response_body = get_all_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)


        if url["requested_resource"] == "comments":
            if url["pk"] != 0:
                response_body = display_comments(pk)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = get_single_user(pk)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = get_all_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "subscription":
            if url["pk"] == 0:
                response_body = get_all_subscriptions()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        if url["requested_resource"] == "reactions":
            if url["pk"] != 0:
                pass
            response_body = get_all_reactions()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)



    def do_PUT(self):
        """Handle PUT requests from a client"""

        content_len = int(self.headers.get("content-length", 0))
        raw_body = self.rfile.read(content_len)
        request_body = json.loads(raw_body)

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "update_comment":
            if pk != 0:
                update_successful = update_comment(request_body, pk)
                return self.response(update_successful, status.HTTP_200_SUCCESS.value)
            content_len = int(self.headers.get('content-length', 0))
            request_body = self.rfile.read(content_len)

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = update_post(pk, request_body)
                if successfully_updated:
                    return self.response(successfully_updated, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                else:
                    return self.response(
                        json.dumps({"error": "Post not found"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )


        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = update_tag(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                else:
                    return self.response(
                        json.dumps({"error": "Tag not found"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                else:
                    return self.response(
                        json.dumps({"error": "Category not found"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )
        
        if url["requested_resource"] == "users":
            if pk != 0:
                successfully_updated = update_user_status(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                else:
                    return self.response(
                        json.dumps({"error": "User not found"}),
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )


    def do_DELETE(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                      
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        elif url["requested_resource"] == "posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
              
        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_deleted = delete_tag(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                      
                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        if url["requested_resource"] == "deleteComment":
            if pk != 0:
                successfully_deleted = delete_comment(pk)
                return self.response(successfully_deleted, status.HTTP_200_SUCCESS.value)
            
        if url["requested_resource"] == "reactions":
            if pk != 0:
                successfully_deleted = delete_reaction(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if url["requested_resource"] == "subscription":
            if url["requested_resource"] != 0:
                successfully_deleted = delete_subscription(pk)
                return self.response(successfully_deleted, status.HTTP_200_SUCCESS.value)



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
         
        if url["requested_resource"] == "post_comments":
            new_comment = create_comment(request_body)
            return self.response(json.dumps(new_comment), status.HTTP_201_SUCCESS_CREATED.value)

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
            
        if url["requested_resource"] == "posts":
            
            new_post_id = create_post(request_body)
            if new_post_id:
                return self.response(
                    json.dumps({ "message": "Post created", "post_id": new_post_id }),
                    status.HTTP_201_SUCCESS_CREATED.value
                )
                  
        
        if url["requested_resource"] == "tags":
            created = create_tag(request_body)
            if created:
                return self.response(created, status.HTTP_201_SUCCESS_CREATED.value)
            
        if url["requested_resource"] == "categories":
            created = create_category(request_body)
            if created:
                return self.response(created, status.HTTP_201_SUCCESS_CREATED.value)
            else:
                return self.response(
                    json.dumps({ "error": "Failed to create category" }),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )
            

        if url["requested_resource"] == "subscription":
            created = create_subscription(request_body)
            if created: 
                    return self.response(created, status.HTTP_201_SUCCESS_CREATED.value)


        if url["requested_resource"] == "reactions":
            created = create_reaction(request_body)
            if created:
                return self.response(created, status.HTTP_201_SUCCESS_CREATED.value)
            
        if url["requested_resource"] == "PostReactions":
            created = add_post_reaction(request_body)
            if created:
                return self.response(created, status.HTTP_201_SUCCESS_CREATED.value)
#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
