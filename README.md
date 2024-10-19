# sandbox

poetry run python -m grpc_tools.protoc \
    -I=application/clients/grpc/protos \
    --mypy_out=readable_stubs,quiet:./application/clients/grpc/account \
    --mypy_grpc_out=readable_stubs,quiet:./application/clients/grpc/account \
    --python_out=./application/clients/grpc/account \
    --grpc_python_out=./application/clients/grpc/account ./application/clients/grpc/protos/account.proto



poetry run python -m grpc_tools.protoc \
    -I=application/clients/grpc/protos/account_proxy \
    --mypy_out=readable_stubs,quiet:./application/clients/grpc/account_proxy \
    --mypy_grpc_out=readable_stubs,quiet:./application/clients/grpc/account_proxy \
    --python_out=./application/clients/grpc/account_proxy \
    --grpc_python_out=./application/clients/grpc/account_proxy ./application/clients/grpc/protos/account_proxy/account_proxy.proto