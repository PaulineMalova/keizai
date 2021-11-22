test:
	flake8 app
	coverage run -m pytest tests

coverage-report:
	coverage report -m pytest tests

coverage-html:
	coverage html

clean:
	rm -rf __pycache__
