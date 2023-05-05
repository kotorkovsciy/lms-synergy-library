VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(PIP) install --upgrade build

build:
	$(PYTHON) -m build

clean:
	rm -rf lms_synergy_library/__pycache__/
	rm -rf lms_synergy_library.egg-info
	rm -rf $(VENV)
