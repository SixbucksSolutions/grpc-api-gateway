# grpc-api-gateway
Proof of concept for gRPC API Gateway

# Source

https://grpc.io/docs/languages/python/quickstart/

# Sample Project

https://github.com/grpc/grpc/tree/master/examples/python/helloworld

# Summary/Overview

A server app runs that is an API Gateway that can handle gRPC
Unary messages. When it receives a gRPC message from the client, it

* JSON encodes the request object into a string
* Calls another method (acting like a Lambda invocation) and passes it the JSON string as a parameter
* Fake lambda function takes its string parameter and recreates the request object
* Fake Lambda function uses the gRPC-created code to create a reply object to the request
* Fake Lambda function JSON encodes the reply object
* Fake Lambda function returns the JSON encoded object back to the caller function (emulating the API GW)
* Fake API GW creates the reply gRPC object from the JSON string returned
* Fake API GW returns the recreated gRPC reply object, which gets transmitted over the wire to the client

# Reqs

* `sudo apt-get -y install python3-pip`
* `pip3 install grpcio grpcio-tools`

# Build Python code for the grpc proto file

* `python3 -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. helloworld.proto`

# Run server

* `python3 greeter_server.py`

# Run client

In another terminal, run the client

* `python3 greeter_client.py`

