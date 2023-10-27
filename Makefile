shell:
	python3 manage.py shell_plus

migration:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver

test:
	python3 -m pytest -k $(TEST) -vv

all-tests:	
	python3 -m pytest -v

poetry:
	poetry shell

format:
	black .