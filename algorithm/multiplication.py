# from algorithm.base import DSPAlgorithm, AlgorithmParam

# def multiply_by_constant(signal, constant: float, new_name=None):
#     # Imported here (not at the top) to avoid a circular import with signal_model.
#     from signal_model import Signal

#     constant = float(constant)
#     new_samples = (signal.samples * constant).tolist()
#     return Signal(
#         signal.indices.tolist(),
#         new_samples,
#         name=new_name or "Result (Multiplication)",
#         alias=f"{constant:g}*{signal.alias}",
#     )
# ALGORITHM = DSPAlgorithm(
#     name="Multiplication (* Constant)",
#     category="single_signal",
#     run_func=multiply_by_constant,
#     params=[
#         AlgorithmParam(
#             name="constant",
#             label="Constant Value (*)",
#             param_type="float",
#             default_value=2.0,
#             min_value=-1000.0,
#             max_value=1000.0,
#             step=0.5
#         )
#     ],
#     description="Multiplies signal samples by a constant: y[n] = c * x[n]"
# )
from algorithm.base import DSPAlgorithm, AlgorithmParam


def multiply_by_constant(signal, constant: float, new_name=None):
    """y[n] = c * x[n]  (indices unchanged)."""
    from signal_model import Signal

    c = float(constant)
    name = new_name or f"Result (x{c:g})"
    return Signal(
        signal.indices.tolist(),
        (signal.samples * c).tolist(),
        name=name,
        alias=f"{c:g}*{signal.alias}"
    )


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