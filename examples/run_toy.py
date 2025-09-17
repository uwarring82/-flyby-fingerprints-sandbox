import os

from flyby.triad import run_triad, TriadThresholds

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data", "toy")
OUT = os.path.join(HERE, "..", "out")

if __name__ == "__main__":
    res = run_triad(DATA, OUT, TriadThresholds())
    print(res)
