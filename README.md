# beachHacks9.0
My submission for BeachHacks 9.0 at CSULB

Note: I will be continuing development in the Timeback-Scheduler repo on my github page, if you are looking for the up-to-date version.

## Setup
After download, ensure that main.py, schedule.py. task.py, gcal.py, and ui.py are all in the same folder

Then, follow these steps:
1. Go to https://console.cloud.google.com
2. Create a new project and enable the Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download the credentials file and rename it to `credentials.json`
5. Place it in the project root
6. Run `pip install -r requirements.txt`
7. Run `python main.py` — a browser window will open to authenticate
