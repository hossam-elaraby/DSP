from algorithm.base import DSPAlgorithm, AlgorithmParam

def multiply_by_constant(signal, constant: float, new_name=None):
    pass

ALGORITHM = DSPAlgorithm(
    name="Multiplication (* Constant)",
    category="single_signal",
    run_func=multiply_by_constant,
    params=[
        AlgorithmParam(
            name="constant",
            label="Constant Value (*)",
            param_type="float",
            default_value=2.0,
            min_value=-1000.0,
            max_value=1000.0,
            step=0.5
        )
    ],
    description="Multiplies signal samples by a constant: y[n] = c * x[n]"
)
