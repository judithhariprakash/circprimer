from flask_wtf import Form
from wtforms import SelectField, StringField

class SearchForm(Form):
    circ_id = SelectField('circ_id', choices=[])
