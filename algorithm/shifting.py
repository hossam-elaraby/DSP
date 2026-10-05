from algorithm.base import DSPAlgorithm, AlgorithmParam


def delay_or_advance(signal, k: int, new_name=None):
    """y[n] = x[n - k].
    k > 0 -> delay   (every index moves right by k)
    k < 0 -> advance (every index moves left by |k|)"""
    from signal_model import Signal

    k = int(k)
    if k > 0:
        kind = f"Delay {k}"
    elif k < 0:
        kind = f"Advance {abs(k)}"
    else:
        kind = "No Shift"

    return Signal(
        (signal.indices + k).tolist(),
        signal.samples.tolist(),
        name=new_name or f"Result ({kind})",
        alias=f"{signal.alias}(n{-k:+d})"
    )


ALGORITHM = DSPAlgorithm(
    name="Delay / Advance [x(n -/+ k)]",
    category="single_signal",
    run_func=delay_or_advance,
    params=[
        AlgorithmParam(
            name="k",
            label="Shift Steps (k) [k>0: delay, k<0: advance]",
            param_type="int",
            default_value=2,
            min_value=-100,
            max_value=100,
            step=1
        )
    ],
    description="Delays (k > 0) or advances (k < 0) signal in time: y[n] = x[n - k]."
)