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
