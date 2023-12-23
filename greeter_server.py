# Copyright 2015 gRPC authors.
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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import json

#import base64
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import google.protobuf.json_format


class MessageProcessingLambdaSimulator:
    def create_hello_reply(encoded_hello_msg_json_string):
        json_obj = json.loads(encoded_hello_msg_json_string)
        print(f"Lambda got JSON encoded object: \n" + json.dumps(json_obj, indent=4, sort_keys=True))

        recreated_request = google.protobuf.json_format.Parse(json.dumps(json_obj), helloworld_pb2.HelloRequest())

        # Creating response object and then serializing it
        response_object = helloworld_pb2.HelloReply(message="Hello, %s!" % recreated_request.name)

        serialized_response_json = google.protobuf.json_format.MessageToJson(response_object)

        return serialized_response_json
    


class GrpcProxy(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logging.info("Got Hello, message, relaying it to the Lambda behind us")
        recreated_hello_request = helloworld_pb2.HelloRequest(name=request.name)
        #serialized_hello_request_protobuf = recreated_hello_request.SerializeToString()
        #serialized_hello_request_base64 = base64.b64encode(serialized_hello_request_protobuf).decode("utf-8")
        serialized_json_request = google.protobuf.json_format.MessageToJson(recreated_hello_request)

        # Relay the base64 encoded protobuf version of the request to the lambda and get basee64-encoded protobuf reply back
        hello_reply_json_string = MessageProcessingLambdaSimulator.create_hello_reply(serialized_json_request)
        hello_reply_json = json.loads(hello_reply_json_string)
        logging.info("Got reply back from Lambda in json:\n" + json.dumps(hello_reply_json, indent=4, sort_keys=True, default=str))

        # Recreate reply object from JSON 
        recreated_response = google.protobuf.json_format.Parse(json.dumps(hello_reply_json), helloworld_pb2.HelloReply())
        return recreated_response


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(GrpcProxy(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    serve()
