import pickle
from pathlib import Path
import time


def pickle_load(fp: Path):
    with open(fp.absolute(), 'rb') as f:
        x = pickle.load(f)
    return x


def pickle_save(x, fp: Path, overwrite=False):
    if fp.exists() and not overwrite:
        t = time.time_ns()
        fp = fp.with_name(f"{fp.stem}_{t}{fp.suffix}")
        print(f"File exists: saving to {fp}")
    with open(fp.absolute(), 'wb') as f:
        pickle.dump(x, f)
