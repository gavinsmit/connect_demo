# Connect Backend

## Project Setup

* You must be in the repo's directory to execute these commands

```sh
python3 -m venv venv              # or python -m venv venv
source venv/bin/activate          # or . venv/bin/activate
pip install -r requirements.txt
python3 app.py                    # or python app.py
```

* After initial startup please close the app to provision the database with the dummy data.

```sh
sqlite3 connect.db < dummy_data.sql
```

* The app can now be started and it is loaded with dummy data.

```sh
python3 app.py                    # or python app.py
```

* The admin page can be viewed by going to http://localhost:5175/