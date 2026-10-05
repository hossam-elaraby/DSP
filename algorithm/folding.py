# from algorithm.base import DSPAlgorithm

# def fold_signal(signal, new_name=None):
#     # Imported here (not at the top) to avoid a circular import with signal_model.
#     from signal_model import Signal

#     # y[n] = x[-n]: negate every index. Signal() re-sorts the pairs ascending,
#     # which also reverses the order of the samples.
#     return Signal(
#         (-signal.indices).tolist(),
#         signal.samples.tolist(),
#         name=new_name or "Result (Fold)",
#         alias=f"{signal.alias}[-n]",
#     )
# ALGORITHM = DSPAlgorithm(
#     name="Fold (Reverse) [x(-n)]",
#     category="single_signal",
#     run_func=fold_signal,
#     params=[],
#     description="Folds signal in time: y[n] = x[-n]"
# )
from algorithm.base import DSPAlgorithm


def fold_signal(signal, new_name=None):
    """y[n] = x[-n]. Indices are negated; the Signal constructor re-sorts them."""
    from signal_model import Signal

    return Signal(
        (-signal.indices).tolist(),
        signal.samples.tolist(),
        name=new_name or "Result (Fold)",
        alias=f"{signal.alias}(-n)"
    )


ALGORITHM = DSPAlgorithm(
    name="Fold (Reverse) [x(-n)]",
    category="single_signal",
    run_func=fold_signal,
    params=[],
    description="Folds signal in time: y[n] = x[-n]"
)