from flask_wtf import Form
from wtforms import SelectField, StringField, TextAreaField

class SearchForm(Form):
    circ_ids = TextAreaField('Please enter upto 10 Circ ids')
