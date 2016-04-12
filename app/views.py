from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Graeme'} #fake user
	posts = [	# fake array of posts
		{
			'author':{'nickname': 'Tom'},
			'body': 'Beautiful day in New York!'
		},
		{
			'author':{'nickname': 'Jenni'},
			'body': 'My husband is amazing!'
		}
	]
	return render_template('index.html',
							#title='Home',
							user=user,
							posts=posts)