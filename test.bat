call venv/scripts/activate
black template_maker tests
mypy template_maker
python -m pytest -sv tests %*
