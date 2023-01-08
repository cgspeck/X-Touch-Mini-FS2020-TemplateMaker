call venv/scripts/activate
black .
mypy
python -m pytest -sv tests %*
