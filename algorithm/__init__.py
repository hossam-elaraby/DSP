from algorithm.base import DSPAlgorithm, AlgorithmParam
from algorithm.addition import add_signals, ALGORITHM as ADDITION_ALGO
from algorithm.subtraction import subtract_signals, ALGORITHM as SUBTRACTION_ALGO
from algorithm.multiplication import multiply_by_constant, ALGORITHM as MULTIPLICATION_ALGO
from algorithm.shifting import delay_or_advance, ALGORITHM as SHIFTING_ALGO
from algorithm.folding import fold_signal, ALGORITHM as FOLDING_ALGO
from algorithm.quantization import quantize_signal, quantize_samples, ALGORITHM as QUANTIZATION_ALGO
from algorithm.generation import generate_signal, continuous_curve 

def get_registered_algorithms():
    return [
        MULTIPLICATION_ALGO,
        SHIFTING_ALGO,
        FOLDING_ALGO,
        ADDITION_ALGO,
        SUBTRACTION_ALGO,
        QUANTIZATION_ALGO,
    ]


__all__ = [
    "DSPAlgorithm",
    "AlgorithmParam",
    "add_signals",
    "subtract_signals",
    "multiply_by_constant",
    "delay_or_advance",
    "fold_signal",
    "quantize_signal",
    "quantize_samples",
    "get_registered_algorithms",
    "generate_signal",
    "continuous_curve"
]

