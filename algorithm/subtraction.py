from algorithm.base import DSPAlgorithm
from algorithm.addition import add_signals
from algorithm.multiplication import multiply_by_constant

def subtract_signals(sig1, sig2, new_name="Result (Subtraction)"):
    neg_sig2 = multiply_by_constant(sig2, -1.0, new_name=f"-({sig2.name})")
    result = add_signals([sig1, neg_sig2], new_name=new_name)
    result.alias = f"{sig1.alias} - {sig2.alias}"
    return result

ALGORITHM = DSPAlgorithm(
    name="Subtraction (-)",
    category="two_signals",
    run_func=subtract_signals,
    params=[],
    description="Subtracts Signal B from Signal A using: A[n] + (-1)*B[n]."
)
