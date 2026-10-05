from algorithm.base import DSPAlgorithm

def fold_signal(signal, new_name=None):
    pass

ALGORITHM = DSPAlgorithm(
    name="Fold (Reverse) [x(-n)]",
    category="single_signal",
    run_func=fold_signal,
    params=[],
    description="Folds signal in time: y[n] = x[-n]"
)
