install: ../requirements.txt
	( \
	python3 -m venv venv; \
	. ./venv/bin/activate; \
	pip install -r requirements.txt; \
	)

run: install
	( \
	. ./venv/bin/activate; \
	uvicorn asgi:app; \
	)

test:
	( \
	. ./venv/bin/activate; \
	pytest tests/test.py; \
	)
