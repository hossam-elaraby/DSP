from algorithm.base import DSPAlgorithm

def add_signals(signals, new_name="Result (Addition)"):
    from signal_model import Signal

    if not signals:
        raise ValueError("At least one signal must be provided for addition.")

    if len(signals) == 1:
        return signals[0].copy(new_name=new_name)

    all_indices = set()
    for sig in signals:
        all_indices.update(sig.indices.tolist())

    sorted_indices = list(range(min(all_indices), max(all_indices) + 1))
    summed_samples = [sum(sig.get_sample(n) for sig in signals) for n in sorted_indices]
    alias = " + ".join(sig.alias for sig in signals)

    return Signal(sorted_indices, summed_samples, name=new_name, alias=alias)

ALGORITHM = DSPAlgorithm(
    name="Addition (+)",
    category="multi_signals",
    run_func=add_signals,
    params=[],
    description="Adds selected signals with zero-padding over the union index range."
)
