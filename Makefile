.PHONY: dev test toy clean

PY?=python

dev:
$(PY) -m pip install -U pip
$(PY) -m pip install -e . -r requirements.txt

test:
$(PY) -m pytest

toy:
$(PY) -m flyby.triad --data-root data/toy --out out

clean:
rm -rf out .pytest_cache .ruff_cache build dist *.egg-info

.PHONY: sim-default sim-strong-patch sim-mains60

sim-default:
	python scripts/run_background_sim.py --T 300 --rf_rms 0.5 --mains 50 \
	 --em_coupling 1e-3 --patch 5 --corr 50 --cps 200 --tint 1.0 \
	 --n_samples 10000 --dt 1e-4 --seed 1

sim-strong-patch:
	python scripts/run_background_sim.py --T 300 --rf_rms 0.5 --mains 50 \
	 --em_coupling 1e-3 --patch 20 --corr 200 --cps 200 --tint 1.0 \
	 --n_samples 10000 --dt 1e-4 --seed 2

sim-mains60:
	python scripts/run_background_sim.py --T 300 --rf_rms 1.5 --mains 60 \
	 --em_coupling 1e-3 --patch 5 --corr 50 --cps 200 --tint 1.0 \
	 --n_samples 10000 --dt 1e-4 --seed 3
