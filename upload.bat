uv build
python -m twine check dist/*
pause
uv publish
pause
python clean_update.py
pause