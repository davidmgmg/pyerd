python app.py

pyinstaller --noconfirm --windowed --icon=icon.ico --add-data "templates;templates" --add-data "static;static" main.py