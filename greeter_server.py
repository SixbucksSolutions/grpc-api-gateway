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

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class MessageProcessingLambdaSimulator:
    def create_hello_reply(encoded_hello_msg):
        print("Got encoded hello message, trying to decode it")

        deserialized_request = helloworld_pb2.HelloRequest.FromString(encoded_hello_msg)
        


        return helloworld_pb2.HelloReply(message="Hello, insert_name_here")
    


class GrpcProxy(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logging.info("Got Hello, message, relaying it to the Lambda behind us")
        recreated_hello_request = helloworld_pb2.HelloRequest(name=request.name)
        serialized_hello_request_protobuf = helloworld_pb2.HelloRequest.SerializeToString(recreated_hello_request)
        hello_reply = MessageProcessingLambdaSimulator.create_hello_reply(serialized_hello_request_protobuf)
        #return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)
        return hello_reply


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
