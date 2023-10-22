update:
	pip --disable-pip-version-check list --outdated --format=json | python3 -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 pip install -U
	pip freeze | sort > requirements.txt
run:
	python3 -m flask run -app application.py