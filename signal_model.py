import os
import numpy as np
from reader import read_signal
from algorithm.addition import add_signals
from algorithm.subtraction import subtract_signals
from algorithm.multiplication import multiply_by_constant
from algorithm.shifting import delay_or_advance
from algorithm.folding import fold_signal


class Signal:
    def __init__(self, indices, samples, name="Signal", alias="X"):
        if len(indices) != len(samples):
            raise ValueError("Indices and samples must have the same length")

        if len(indices) > 0:
            combined = sorted(zip(indices, samples), key=lambda item: item[0])
            self.indices = np.array([int(idx) for idx, _ in combined], dtype=int)
            self.samples = np.array([float(val) for _, val in combined], dtype=float)
        else:
            self.indices = np.array([], dtype=int)
            self.samples = np.array([], dtype=float)

        self.name = name
        self.alias = alias

    @property
    def n_samples(self):
        return len(self.samples)

    @property
    def min_index(self):
        return int(np.min(self.indices)) if len(self.indices) > 0 else 0

    @property
    def max_index(self):
        return int(np.max(self.indices)) if len(self.indices) > 0 else 0

    def to_dict(self):
        return {int(idx): float(val) for idx, val in zip(self.indices, self.samples)}

    def get_sample(self, n):
        idx_pos = np.where(self.indices == n)[0]
        if len(idx_pos) > 0:
            return float(self.samples[idx_pos[0]])
        return 0.0

    def copy(self, new_name=None, new_alias=None):
        return Signal(
            indices=self.indices.tolist(),
            samples=self.samples.tolist(),
            name=new_name or self.name,
            alias=new_alias or self.alias
        )

    def __repr__(self):
        return f"Signal({self.name}, {self.alias}, N={self.n_samples})"


def read_signal_from_file(file_path, default_name=None, default_alias=None):
    indices, samples = read_signal(file_path)
    if not indices:
        raise ValueError(f"Could not parse valid sample data from '{file_path}'.")
    name = default_name or os.path.splitext(os.path.basename(file_path))[0]
    alias = default_alias or "X"
    return Signal(indices, samples, name=name, alias=alias)


def write_signal_to_file(signal, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("0\n")
        f.write("0\n")
        f.write(f"{signal.n_samples}\n")
        for idx, val in zip(signal.indices, signal.samples):
            f.write(f"{int(idx)} {val:.6f}\n")
