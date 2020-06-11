test:
	pytest -vv --cov=starlette_x_bugsnag --cov-report=term-missing --junitxml=.junit/test-results.xml

isort:
	isort --recursive .

black:
	black .

format: isort black

lint-isort:
	isort --recursive --check-only .

lint-black:
	black --check .

lint-mypy:
	mypy .

lint-safety:
	safety check --full-report

lint: lint-isort lint-black lint-mypy lint-safety
