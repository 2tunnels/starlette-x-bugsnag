test:
	pytest -vv --cov=starlette_x_bugsnag --cov-report=term-missing --cov-report=xml

isort:
	isort .

black:
	black .

format: isort black

lint-isort:
	isort --check-only .

lint-black:
	black --check .

lint-mypy:
	mypy .

lint-safety:
	safety check --full-report

lint: lint-isort lint-black lint-mypy lint-safety

patch:
	bump2version patch
	git push --follow-tags

publish:
	poetry publish --build
