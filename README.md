Installed things from terminal:
-pip install flask
-pip install python-dotenv
-pip install flask-wtf
-pip install flask-sqlalchemy: provides flask friendly wrapper to sqlalchemy which is ORM; allow apps to manage a database using classes, objects, methods instead of tables and sql. Supports sqlite, mysql, postgresql.
-pip install flask-migrate: a flask wrapper for alembic, a database migration framework for sqlalchemy. First time use run flask db init.
-pip install flask-login: manages the user logged-in state and remember me
-pip install email-validator: stock validator that comes with WTForms, will ensure the structure of email address
-pip install flask-mail: to send emails eg authentication issues
-pip install pyjwt: password reset links will have secure token, so to generate these tokens, we need JSON Web Tokens


---To activate virtual environment: ---
source .venv/bin/activate

To run flask:
flask run

To start python interpreter:
flask shell

Migrations (do these while in venv):
-generate automatic migration: flask db migrate -m "comment"
-then to apply changes: flask db upgrade
(note: Flask-SQLAlchemy uses snake case, so User becomes user, AddressAndPhone -> address_and_phone)

NOTE: Whenever changing MODELS, always generate database migration!!!!

Things that I'm skipping...
-avatar, part vi. should add logic to user model.
