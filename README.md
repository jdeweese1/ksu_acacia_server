# acacia_server

This project is the server backend for slack at Acacia Fraternity at K-State.

## Running the project 
```brew install python```

```pip install virtualenv```

# Environment variables
``````
FLASK_APP=autoapp.py
FLASK_DEBUG=1
FLASK_ENV=development
DATABASE_URL=sqlite:////tmp/dev.db
GUNICORN_WORKERS=1
LOG_LEVEL=debug
SECRET_KEY=some_secret_key
SEND_FILE_MAX_AGE_DEFAULT=0 # In production, set to a higher number, like 31556926
SLACK_TOKEN=some slack token
CLEANING_DUTIES_CHANNEL=slack channel cleaning duties should be posted in
A_WEST_CHANNEL=channel of people who live in the annex
```

