.PHONY: install test lint clean run

install:
	pip install -e . pytest

test:
	pytest -q

lint:
	python -m compileall -q src

run:
	python -m nucleus_patch_utility_2026

clean:
	rm -rf build dist *.egg-info __pycache__
