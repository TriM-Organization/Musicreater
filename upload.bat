python -m build
python -m twine upload dist/*
python clean_update.py
