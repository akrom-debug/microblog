import sqlalchemy as sa #type: ignore
import sqlalchemy.orm as so #type: ignore
from app import app, db
from app import cli
from app import translate
from app.models import User, Post

translate.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}