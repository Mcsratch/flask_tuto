from flask import Flask, flash, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://matco:Chang/9/@localhost/flaskdb'
db.init_app(app)

app.secret_key = "development"

@app.route("/")
def index():
 return render_template("index.html")
 #return render_template("7trees.html")


@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/home")
def home(email=None):
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    return render_template("home.html", email=email)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
      return redirect(url_for('home'))
    form=LoginForm()
    if request.method == "POST":
        if form.validate() == False:
          return render_template('login.html', form=form)
        else:
          email = form.email.data
          password = form.password.data
          user = User.query.filter_by(email=email).first()
          if user is not None and user.check_password(password):
              session['email'] = form.email.data
              return redirect(url_for('home'))
          else:
              message = "Invalid Login or Password credentials"
              #return redirect(url_for('login'), message=message)
              return render_template('login.html' , form=form, message = message)
    elif request.method == "GET":
        return render_template('login.html', form=form)
@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('You are now logged out')
    return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug=True)
