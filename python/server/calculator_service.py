import logging

import calculator_pb2
import calculator_pb2_grpc
import grpc

from operations import ArithmeticOperations

class Calculator(calculator_pb2_grpc.CalculatorServicer):
    """
    Implements the Calculator gRPC service.
    """

    def Calculate(self, request: calculator_pb2.BinaryOperation, context: grpc.ServicerContext) -> calculator_pb2.CalculationResult:
        """
        Performs calculation based on the request.
        """
        logging.info(f"Received request: {request}")

        try:
            result = ArithmeticOperations.calculate(request.first_operand, request.second_operand, request.operation)
            return calculator_pb2.CalculationResult(result=result)
        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            return calculator_pb2.CalculationResult()