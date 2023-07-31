python setup.py sdist bdist_wheel
python -m twine upload dist/*
python clean_update.py
