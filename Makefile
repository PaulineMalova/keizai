MINIMUM_CODE_COVERAGE ?=70

install: requirements.txt
	pip install -r requirements.txt

test:
	flake8 app
	coverage run -m pytest tests

coverage-report:
	coverage report -m --fail-under=$(MINIMUM_CODE_COVERAGE)

coverage-html:
	coverage html --fail-under=$(MINIMUM_CODE_COVERAGE)

clean:
	rm -rf __pycache__
