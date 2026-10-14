import os
import io
import importlib.util
from contextlib import redirect_stdout

from reader import read_signal, find_file_ci
from signal_model import Signal
from algorithm.addition import add_signals
from algorithm.subtraction import subtract_signals
from algorithm.multiplication import multiply_by_constant
from algorithm.shifting import delay_or_advance
from algorithm.folding import fold_signal
from algorithm.quantization import quantize_signal

TASK_SUBPATH = ("tasks", "Lab 1", "Task 1 testcases and testing functions")
TEST_SCRIPT = "DSP Task TEST functions.py"


def _error(name, message):
    return [{"name": name, "passed": False, "message": message,
             "result_signal": None, "s1": None, "s2": None}]


def get_task_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(base_dir, *TASK_SUBPATH)
    if os.path.isdir(candidate):
        return candidate
    for root, _dirs, files in os.walk(base_dir):
        if any(f.lower() == TEST_SCRIPT.lower() for f in files):
            return root
    return ""


def _run_cases(mod, s1, s2):
    tests = [
        ("Addition (Signal1 + Signal2 -> add.txt)",
         lambda: add_signals([s1, s2]),
         lambda r: mod.AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", r.indices.tolist(), r.samples.tolist())),
        ("Subtraction (Signal1 - Signal2 -> subtract.txt)",
         lambda: subtract_signals(s1, s2),
         lambda r: mod.SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", r.indices.tolist(), r.samples.tolist())),
        ("Multiplication (Signal1 * 5 -> mul5.txt)",
         lambda: multiply_by_constant(s1, 5),
         lambda r: mod.MultiplySignalByConst(5, r.indices.tolist(), r.samples.tolist())),
        # test "3" means x(n+3) = advance;  our k<0 = advance
        ("Advance 3 (Shift_value=3 -> advance3.txt)",
         lambda: delay_or_advance(s1, -3),
         lambda r: mod.ShiftSignalByConst(3, r.indices.tolist(), r.samples.tolist())),
        ("Delay 3 (Shift_value=-3 -> delay3.txt)",
         lambda: delay_or_advance(s1, 3),
         lambda r: mod.ShiftSignalByConst(-3, r.indices.tolist(), r.samples.tolist())),
        ("Folding (x(-n) -> folding.txt)",
         lambda: fold_signal(s1),
         lambda r: mod.Folding(r.indices.tolist(), r.samples.tolist())),
    ]

    results = []
    for test_name, calc_func, test_func in tests:
        try:
            res_signal = calc_func()
            buf = io.StringIO()
            with redirect_stdout(buf):
                test_func(res_signal)
            out = buf.getvalue().strip()
            results.append({
                "name": test_name,
                "passed": "passed successfully" in out.lower(),
                "message": out,
                "result_signal": res_signal,
                "s1": s1,
                "s2": s2,
            })
        except Exception as e:
            results.append({
                "name": test_name,
                "passed": False,
                "message": f"Error: {e}",
                "result_signal": None,
                "s1": s1,
                "s2": s2,
            })
    return results


def run_lab1_tests():
    task_dir = get_task_dir()
    if not task_dir:
        return _error("Environment", "Task testcases directory not found.")

    s1_path = find_file_ci(task_dir, "Signal1.txt")
    s2_path = find_file_ci(task_dir, "Signal2.txt")
    script = find_file_ci(task_dir, TEST_SCRIPT)
    if not s1_path or not s2_path:
        return _error("Files", "Signal1.txt or Signal2.txt not found.")
    if not script:
        return _error("Files", f"'{TEST_SCRIPT}' not found.")

    s1 = Signal(*read_signal(s1_path), name="Signal1", alias="X")
    s2 = Signal(*read_signal(s2_path), name="Signal2", alias="Y")

    orig_dir = os.getcwd()
    try:
        # the test script opens add.txt, mul5.txt ... relative to the cwd
        os.chdir(task_dir)
        spec = importlib.util.spec_from_file_location("test_funcs", script)
        mod = importlib.util.module_from_spec(spec)
        mod.__dict__["indicies"] = []   # the script calls its checks once at import time
        mod.__dict__["samples"] = []
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
        return _run_cases(mod, s1, s2)
    except Exception as e:
        return _error("Loader", f"Error loading test functions: {e}")
    finally:
        os.chdir(orig_dir)


def run_lab3_tests():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lab3_dir = os.path.join(base_dir, "tasks", "Lab 3")
    if not os.path.isdir(lab3_dir):
        return _error("Environment", "Lab 3 directory not found.")

    results = []
    orig_dir = os.getcwd()

    # Test 1: Bits = 3
    t1_dir = os.path.join(lab3_dir, "Test 1")
    t1_input = find_file_ci(t1_dir, "Quan1_input.txt")
    t1_out = find_file_ci(t1_dir, "Quan1_Out.txt")
    t1_script = find_file_ci(t1_dir, "QuanTest1.py")
    if t1_input and t1_out and t1_script:
        try:
            s1 = Signal(*read_signal(t1_input), name="Quan1_Input", alias="X")
            res_signal = quantize_signal(s1, mode="bits", num_bits=3)
            os.chdir(t1_dir)
            spec = importlib.util.spec_from_file_location("quan_test1", t1_script)
            mod1 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod1)

            buf = io.StringIO()
            with redirect_stdout(buf):
                mod1.QuantizationTest1(
                    t1_out,
                    res_signal.quantization_data["encoded_values"],
                    res_signal.quantization_data["quantized_values"]
                )
            out = buf.getvalue().strip()
            results.append({
                "name": "Lab 3 - Test 1 (Bits = 3 -> Quan1_Out.txt)",
                "passed": "passed successfully" in out.lower(),
                "message": out,
                "result_signal": res_signal,
                "s1": s1,
                "s2": None,
            })
        except Exception as e:
            results.append({
                "name": "Lab 3 - Test 1 (Bits = 3 -> Quan1_Out.txt)",
                "passed": False,
                "message": f"Error: {e}",
                "result_signal": None,
                "s1": None,
                "s2": None,
            })
        finally:
            os.chdir(orig_dir)
    else:
        results.append({
            "name": "Lab 3 - Test 1",
            "passed": False,
            "message": "Test 1 files not found.",
            "result_signal": None,
            "s1": None,
            "s2": None,
        })

    # Test 2: Levels = 4
    t2_dir = os.path.join(lab3_dir, "Test 2")
    t2_input = find_file_ci(t2_dir, "Quan2_input.txt")
    t2_out = find_file_ci(t2_dir, "Quan2_Out.txt")
    t2_script = find_file_ci(t2_dir, "QuanTest2.py")
    if t2_input and t2_out and t2_script:
        try:
            s2 = Signal(*read_signal(t2_input), name="Quan2_Input", alias="X")
            res_signal2 = quantize_signal(s2, mode="levels", num_levels=4)
            os.chdir(t2_dir)
            spec2 = importlib.util.spec_from_file_location("quan_test2", t2_script)
            mod2 = importlib.util.module_from_spec(spec2)
            spec2.loader.exec_module(mod2)

            buf = io.StringIO()
            with redirect_stdout(buf):
                mod2.QuantizationTest2(
                    t2_out,
                    res_signal2.quantization_data["interval_indices"],
                    res_signal2.quantization_data["encoded_values"],
                    res_signal2.quantization_data["quantized_values"],
                    res_signal2.quantization_data["error_values"]
                )
            out = buf.getvalue().strip()
            results.append({
                "name": "Lab 3 - Test 2 (Levels = 4 -> Quan2_Out.txt)",
                "passed": "passed successfully" in out.lower(),
                "message": out,
                "result_signal": res_signal2,
                "s1": s2,
                "s2": None,
            })
        except Exception as e:
            results.append({
                "name": "Lab 3 - Test 2 (Levels = 4 -> Quan2_Out.txt)",
                "passed": False,
                "message": f"Error: {e}",
                "result_signal": None,
                "s1": None,
                "s2": None,
            })
        finally:
            os.chdir(orig_dir)
    else:
        results.append({
            "name": "Lab 3 - Test 2",
            "passed": False,
            "message": "Test 2 files not found.",
            "result_signal": None,
            "s1": None,
            "s2": None,
        })

    return results


def run_all_lab_tests(lab="all"):
    if lab == "lab1":
        return run_lab1_tests()
    elif lab == "lab3":
        return run_lab3_tests()
    return run_lab1_tests() + run_lab3_tests()
