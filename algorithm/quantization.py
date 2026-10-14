import math
from algorithm.base import DSPAlgorithm
from signal_model import Signal


def quantize_samples(samples, num_levels=None):
    if num_levels is None:
        raise ValueError("Must specify num_levels")
    l = int(num_levels)
    b = int(math.ceil(math.log2(l)))
    min_val = float(min(samples))
    max_val = float(max(samples))
    delta = (max_val - min_val) / l if l > 0 else 0.0

    interval_indices = []
    encoded_values = []
    quantized_values = []
    error_values = []

    for x in samples:
        if delta == 0:
            idx = 0
            midpoint = min_val
        else:
            idx = int((x - min_val) / delta)
            idx = min(idx, l - 1)
            idx = max(idx, 0)
            midpoint = min_val + (idx + 0.5) * delta

        code = format(idx, f"0{b}b")
        err = midpoint - x

        interval_indices.append(idx + 1)
        encoded_values.append(code)
        quantized_values.append(round(midpoint, 3))
        error_values.append(round(err, 3))

    return interval_indices, encoded_values, quantized_values, error_values


def quantize_signal(signal, mode="bits", num_bits=3, num_levels=8, new_name=None, new_alias=None):
    if len(signal.samples) == 0:
        raise ValueError("Cannot quantize an empty signal")

    if mode == "bits":
        b = int(num_bits)
        l = 2 ** b
    else:
        l = int(num_levels)
        b = int(math.ceil(math.log2(l)))

    interval_idx, encoded, quantized, errors = quantize_samples(signal.samples, num_levels=l)
    min_val = float(min(signal.samples))
    max_val = float(max(signal.samples))
    delta = (max_val - min_val) / l if l > 0 else 0.0

    name = new_name or f"{signal.alias}_Quantized"
    alias = new_alias or f"{signal.alias}_Quantized"

    res_sig = Signal(
        indices=signal.indices.tolist(),
        samples=quantized,
        name=name,
        alias=alias
    )

    res_sig.quantization_data = {
        "num_bits": b,
        "num_levels": l,
        "delta": delta,
        "min_val": min_val,
        "max_val": max_val,
        "interval_indices": interval_idx,
        "encoded_values": encoded,
        "quantized_values": quantized,
        "error_values": errors,
        "original_samples": signal.samples.tolist()
    }

    res_sig.error_signal = Signal(
        indices=signal.indices.tolist(),
        samples=errors,
        name=f"{signal.alias}_Error",
        alias=f"{signal.alias}_Error"
    )

    return res_sig


ALGORITHM = DSPAlgorithm(
    name="Quantization",
    category="conversion",
    run_func=quantize_signal,
    params=[],
    description="Quantizes signal samples "
)
