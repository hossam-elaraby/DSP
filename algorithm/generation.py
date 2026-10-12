import numpy as np
from signal_model import Signal

MAX_SAMPLES = 200_000

def generate_signal(kind, amplitude, phase, analog_freq, sampling_freq,
                    duration=1.0, name=None, alias="X", periods=None):
    """Generate a sine or cosine signal.

    If periods is provided, duration is calculated as periods / analog_freq.
    Otherwise, the supplied duration is used.
    Phase (theta) is in radians.
    """
    if kind not in ("sin", "cos"):
        raise ValueError("kind must be 'sin' or 'cos'")

    if analog_freq <= 0:
        raise ValueError("Analog frequency must be greater than 0.")

    if sampling_freq < 2 * analog_freq:
        raise ValueError(
            f"Sampling theorem violated: fs ({sampling_freq} Hz) must be at least "
            f"2 x f ({2 * analog_freq} Hz)."
        )

    if periods is not None:
        if periods <= 0:
            raise ValueError("Number of periods must be greater than 0.")
        duration = periods / analog_freq

    if duration <= 0:
        raise ValueError("Duration must be greater than 0.")

    n_samples = int(round(sampling_freq * duration))

    if n_samples < 1 or n_samples > MAX_SAMPLES:
        raise ValueError(
            f"Number of samples must be between 1 and {MAX_SAMPLES}."
        )

    n = np.arange(n_samples)
    arg = 2 * np.pi * (analog_freq / sampling_freq) * n + phase
    y = amplitude * (
        np.sin(arg) if kind == "sin" else np.cos(arg)
    )

    label = "Sine" if kind == "sin" else "Cosine"

    return Signal(
        n.tolist(),
        y.tolist(),
        name=name or label,
        alias=alias,
        fs=sampling_freq,
        params={
            "kind": kind,
            "A": amplitude,
            "theta": phase,
            "f": analog_freq,
            "duration": duration,
            "periods": duration * analog_freq,
        },
    )


def continuous_curve(sig, points_per_sample=20):
    """Dense analytic curve (t, y) for a generated sinusoid, for continuous display."""
    p = sig.params
    t = np.linspace(sig.indices[0] / sig.fs, sig.indices[-1] / sig.fs,
                    max(2, sig.n_samples * points_per_sample))
    arg = 2 * np.pi * p["f"] * t + p["theta"]
    y = p["A"] * (np.sin(arg) if p["kind"] == "sin" else np.cos(arg))
    return t, y