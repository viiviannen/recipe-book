# FLASKENV Purpose: Used to configure Flask's runtime behavior (e.g., application entry point, 
# debug mode, etc.) and store environment variables for the application.
# How it works: Flask's python-dotenv package reads the .flaskenv file 
# automatically when the app runs, and its contents are loaded into the environment.

FLASK_APP=recipebook.py
FLASK_ENV=development
FLASK_DEBUG=1 

MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=9537a21ed705cf
MAIL_PASSWORD=f3609cd34b75df