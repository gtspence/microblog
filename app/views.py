from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

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
							title='Home',
							user=user,
							posts=posts)
							
@app.route('/login', methods=['GET', 'POST']) #methods=POST allows form data stored
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %
				(form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html',
							title='Sign In',
							form=form,
							providers=app.config['OPENID_PROVIDERS'])