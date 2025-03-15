from typing import Callable, Dict

import calculator_pb2

# Operation Mapping
OPERATIONS: Dict[int, Callable[[float, float], float]] = {
    calculator_pb2.ADD: lambda x, y: x + y,
    calculator_pb2.SUBTRACT: lambda x, y: x - y,
    # Add more operations here in the future.
}

class ArithmeticOperations:
    """
    Provides arithmetic operation logic.
    """
    @staticmethod
    def calculate(operand1: float, operand2: float, operation: int) -> float:
        """
        Performs arithmetic operation based on the operation type.
        """
        if operation in OPERATIONS:
            return OPERATIONS[operation](operand1, operand2)
        else:
            raise ValueError("Unsupported operation.")