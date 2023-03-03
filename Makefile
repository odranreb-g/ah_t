test:
	poetry run python ah_t/tests/pre_test.py
	poetry run pytest ah_t -v -x --pdb --cov=ah_t --cov-report html

runserver:
	poetry run uvicorn ah_t.main:app --reload
