import argparse
import logging
from typing import Text

import grpc

import calculator_pb2
import calculator_pb2_grpc

# Constants
OPERATIONS = {
    "add": calculator_pb2.ADD,
    "subtract": calculator_pb2.SUBTRACT,
}

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_grpc_channel(server_address: Text, plaintext: bool) -> grpc.Channel:
    """Creates a gRPC channel."""
    if plaintext:
        logging.info(f"Creating insecure channel to {server_address}")
        return grpc.insecure_channel(server_address)
    else:
        logging.info(f"Creating secure channel to {server_address}")
        return grpc.secure_channel(server_address, grpc.ssl_channel_credentials())


def calculate(server_address: Text, operation: calculator_pb2.Operation, a: float, b: float, plaintext: bool) -> float:
    """Performs a calculation using gRPC."""
    try:
        with create_grpc_channel(server_address, plaintext) as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            request = calculator_pb2.BinaryOperation(first_operand=a, second_operand=b, operation=operation)
            response = stub.Calculate(request)
            logging.info(f"Calculation result: {response.result}")
            return response.result
    except grpc.RpcError as e:
        logging.error(f"gRPC error: {e}")
        return None  # Or raise the exception, depending on your error handling policy.
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="gRPC Calculator Client")
    parser.add_argument("server", help="The address of the calculator server.")
    parser.add_argument("operation", choices=OPERATIONS.keys(), help="The operation to perform")
    parser.add_argument("a", type=float, help="The first operand.")
    parser.add_argument("b", type=float, help="The second operand.")
    parser.add_argument("-k", "--plaintext", action="store_true", help="Use a plaintext connection.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    result = calculate(args.server, OPERATIONS[args.operation], args.a, args.b, args.plaintext)
    if result is not None:
        print(result)