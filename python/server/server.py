import logging
import os
from concurrent import futures
from typing import Text

import grpc

import calculator_pb2_grpc
from calculator_service import Calculator

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Constants
DEFAULT_PORT = "8080"
PORT_ENV_VAR = "PORT"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def serve(port: Text) -> None:
    """
    Starts the gRPC server.
    """
    bind_address = f"[::]:{port}"
    server = grpc.server(futures.ThreadPoolExecutor())
    calculator_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    server.add_insecure_port(bind_address)
    server.start()
    logging.info(f"Listening on {bind_address}.")
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get(PORT_ENV_VAR, DEFAULT_PORT)
    serve(port)