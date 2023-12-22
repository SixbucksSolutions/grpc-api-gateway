# Can we compile our own PB files?

# Reqs

* `sudo apt-get -y install python3-pip`
* `pip3 install grpcio grpcio-tools`

# Compile proto

* `cd proto`
* `python3 -m grpc_tools.protoc -I. --python_out=.. --pyi_out=.. --grpc_python_out=.. helloworld.proto`
* `cd ..`
* `python3 greeter_server.py`
* `python3 greeter_client.py`

And it all works!

