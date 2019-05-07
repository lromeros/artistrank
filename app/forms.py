from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchArtistForm(FlaskForm):
    """"A FlaskForm representing the initial artist search interaction."""
    search_artist = StringField("Search Artist", validators=[DataRequired()])
