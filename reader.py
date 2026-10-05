# def read_signal(file_path):
#     indices = []
#     samples = []
#     with open(file_path, 'r') as f:
#         for line in f:
#             parts = line.strip().split()
#             if len(parts) == 2:
#                 try:
#                     indices.append(int(float(parts[0])))
#                     samples.append(float(parts[1]))
#                 except ValueError:
#                     continue
#     return indices, samples

# def ReadSignalFile(file_name):
#     return read_signal(file_name)
import os


def read_signal(file_path):
    """Reads a signal file. Any line that is not exactly 'index value' is
    treated as header (works with both the 1-line N header and the 3-line
    lab header: type / periodic / N)."""
    indices = []
    samples = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.replace(',', ' ').split()
            if len(parts) == 2:
                try:
                    indices.append(int(float(parts[0])))
                    samples.append(float(parts[1]))
                except ValueError:
                    continue
    return indices, samples


def ReadSignalFile(file_name):
    return read_signal(file_name)


def find_file_ci(directory, filename):
    """Case-insensitive file lookup (Signal1.txt vs signal1.txt on Linux/macOS)."""
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        return path
    target = filename.lower()
    try:
        for entry in os.listdir(directory):
            if entry.lower() == target:
                return os.path.join(directory, entry)
    except OSError:
        pass
    return None