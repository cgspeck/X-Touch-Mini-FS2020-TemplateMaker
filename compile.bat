call venv/scripts/activate
python -m scripts.make_version_file
pyinstaller --noconfirm main.spec
