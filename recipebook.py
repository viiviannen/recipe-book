import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Recipe

# creates a shell context that adds database instance and models to the shell session when run 'flask shell'
@app.shell_context_processor 
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Recipe': Recipe}