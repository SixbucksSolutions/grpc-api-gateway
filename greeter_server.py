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

import base64
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class MessageProcessingLambdaSimulator:
    def create_hello_reply(encoded_hello_msg_b64):
        print(f"Lambda got base64 encoded protobuf: \"{encoded_hello_msg_b64}\"")

        encoded_hello_msg_protobuf = base64.b64decode(encoded_hello_msg_b64)
        print(f"Lambda decoded base64 parameter into protobuf-encoded hello message: \"{encoded_hello_msg_protobuf}\"")

        recreated_request = helloworld_pb2.HelloRequest.FromString(encoded_hello_msg_protobuf)

        # Creating response object and then serializing it
        response_object = helloworld_pb2.HelloReply(message="Hello, %s!" % recreated_request.name)

        print("Created response object (JSON format): " + json.dumps(response_object, indent=4, sort_keys=True, default=str))

        serialized_response_protobuf = response_object.SerializeToString()

        serialized_response_base64 = base64.b64encode(serialized_response_protobuf).decode("utf-8")

        #return helloworld_pb2.HelloReply(message="Hello, insert_name_here")
        return serialized_response_base64
    


class GrpcProxy(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logging.info("Got Hello, message, relaying it to the Lambda behind us")
        recreated_hello_request = helloworld_pb2.HelloRequest(name=request.name)
        #serialized_hello_request_protobuf = helloworld_pb2.HelloRequest.SerializeToString(recreated_hello_request)
        serialized_hello_request_protobuf = recreated_hello_request.SerializeToString()
        serialized_hello_request_base64 = base64.b64encode(serialized_hello_request_protobuf).decode("utf-8")

        # Relay the base64 encoded protobuf version of the request to the lambda and get basee64-encoded protobuf reply back
        hello_reply_base64 = MessageProcessingLambdaSimulator.create_hello_reply(serialized_hello_request_base64)
        logging.info(f"Got reply back from Lambda in base64: \"{hello_reply_base64}\"")

        # Decode base64 which will give us raw protobuf
        hello_reply_protobuf = base64.b64decode(hello_reply_base64)

        # Turn protobuf from lambda into a valid reply object and ship it back out to the client
        recreated_response = helloworld_pb2.HelloReply.FromString(hello_reply_protobuf)
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
