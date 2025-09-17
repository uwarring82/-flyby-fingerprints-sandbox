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
