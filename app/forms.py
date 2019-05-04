from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchArtistForm(FlaskForm):
    search_artist = StringField('Search Artist', validators=[DataRequired()])
