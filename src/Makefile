setup:
	python3 -m venv ~/.volatrader && source ~/.volatrader/bin/activate

install:
	pip install -r ../requirements.txt

test:
	python -m pytest -vv tests/*.py

lint:
	cd src && python -m pylint *

all: install lint test