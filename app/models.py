from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login, app
from time import time
import jwt

# UserMixin provides default implementations for the methods that Flask-Login expects user objects to have
# db.Model is the base class for all models in SQLAlchemy
class User(UserMixin, db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    recipes: so.Mapped['Recipe'] = so.relationship(back_populates='author')

    # repr method tells python how to print objects of this class, useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # password hashing and verification
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # password reset token generation and verification
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

# user_loader callback is registered with Flask-Login to load a user by ID
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
  
class Recipe(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    ingredients: so.Mapped[str] = so.mapped_column(sa.Text)
    instructions: so.Mapped[str] = so.mapped_column(sa.Text)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='recipes')

    def __repr__(self):
        return f"<Recipe {self.name}>"