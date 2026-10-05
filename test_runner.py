import os
import sys
import io
import importlib.util
from contextlib import redirect_stdout
from reader import read_signal
from signal_model import Signal
from algorithm.addition import add_signals
from algorithm.subtraction import subtract_signals
from algorithm.multiplication import multiply_by_constant
from algorithm.shifting import delay_or_advance
from algorithm.folding import fold_signal


def get_task_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(base_dir, "tasks", "Lab 1", "Task 1 testcases and testing functions")
    if os.path.exists(candidate):
        return candidate
    for root, dirs, files in os.walk(base_dir):
        if "DSP Task TEST functions.py" in files:
            return root
    return ""


def run_lab1_tests():
    task_dir = get_task_dir()
    if not task_dir:
        return [{"name": "Environment", "passed": False, "message": "Task testcases directory not found."}]

    orig_dir = os.getcwd()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    s1_path = os.path.join(task_dir, "Signal1.txt")
    s2_path = os.path.join(task_dir, "Signal2.txt")
    if not os.path.exists(s1_path) or not os.path.exists(s2_path):
        return [{"name": "Files", "passed": False, "message": "Signal1.txt or Signal2.txt not found."}]

    s1_idx, s1_samp = read_signal(s1_path)
    s2_idx, s2_samp = read_signal(s2_path)
    s1 = Signal(s1_idx, s1_samp, name="Signal1", alias="X")
    s2 = Signal(s2_idx, s2_samp, name="Signal2", alias="Y")

    os.chdir(task_dir)
    try:
        spec = importlib.util.spec_from_file_location("test_funcs", "DSP Task TEST functions.py")
        mod = importlib.util.module_from_spec(spec)
        mod.__dict__["indicies"] = []
        mod.__dict__["samples"] = []
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
    except Exception as e:
        os.chdir(orig_dir)
        return [{"name": "Loader", "passed": False, "message": f"Error loading test functions: {e}"}]

    tests = [
        ("Addition (Signal1 + Signal2 -> add.txt)", lambda: add_signals([s1, s2]),
         lambda res: mod.AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", res.indices.tolist(), res.samples.tolist())),
        ("Subtraction (Signal1 - Signal2 -> subtract.txt)", lambda: subtract_signals(s1, s2),
         lambda res: mod.SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", res.indices.tolist(), res.samples.tolist())),
        ("Multiplication (Signal1 * 5 -> mul5.txt)", lambda: multiply_by_constant(s1, 5),
         lambda res: mod.MultiplySignalByConst(5, res.indices.tolist(), res.samples.tolist())),
        ("Advance 3 (Shift_value=3 -> advance3.txt)", lambda: delay_or_advance(s1, -3),
         lambda res: mod.ShiftSignalByConst(3, res.indices.tolist(), res.samples.tolist())),
        ("Delay 3 (Shift_value=-3 -> delay3.txt)", lambda: delay_or_advance(s1, 3),
         lambda res: mod.ShiftSignalByConst(-3, res.indices.tolist(), res.samples.tolist())),
        ("Folding (x(-n) -> folding.txt)", lambda: fold_signal(s1),
         lambda res: mod.Folding(res.indices.tolist(), res.samples.tolist())),
    ]

    results = []
    for test_name, calc_func, test_func in tests:
        try:
            res_signal = calc_func()
            buf = io.StringIO()
            with redirect_stdout(buf):
                test_func(res_signal)
            out = buf.getvalue().strip()
            passed = "passed successfully" in out.lower()
            results.append({
                "name": test_name,
                "passed": passed,
                "message": out,
                "result_signal": res_signal,
                "s1": s1,
                "s2": s2
            })
        except Exception as e:
            results.append({
                "name": test_name,
                "passed": False,
                "message": f"Error: {e}",
                "result_signal": None,
                "s1": s1,
                "s2": s2
            })

    os.chdir(orig_dir)
    return results
