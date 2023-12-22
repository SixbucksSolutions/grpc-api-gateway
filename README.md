# grpc-api-gateway
Proof of concept for gRPC API Gateway

# Source

https://grpc.io/docs/languages/python/quickstart/

# Sample Project

https://github.com/grpc/grpc/tree/master/examples/python/helloworld

# Reqs

* `sudo apt-get -y install python3-pip`
* `pip3 install grpcio grpcio-tools`

# Build Python code for the grpc proto file

* `python3 -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. helloworld.proto`

