def read_signal(file_path):
    indices = []
    samples = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    indices.append(int(float(parts[0])))
                    samples.append(float(parts[1]))
                except ValueError:
                    continue
    return indices, samples

def ReadSignalFile(file_name):
    return read_signal(file_name)
