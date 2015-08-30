from circprimer import app
from flask import render_template
from forms import SearchForm


@app.route('/', methods = ['GET', 'POST'])
def index():
	form = SearchForm()
	return render_template('index.html', form=form)


@app.route('/<circid>')
def get_circ_id(circid):
	pass
