import os

from flask import render_template, send_from_directory, request, Response, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from main import app, login_manager, db
from models import Run, User

here = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def home():
    Run.clearDone()
    stats = {"runs": len(Run.query.all()), "runners": len(User.query.all())}
    context = {"upcoming_runs": Run.query.order_by("time").all(), "stats": stats, }
    return render_template("index.html", context=context)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        remember = False
        if request.form.get('rem'):
            remember = True
        print(remember)
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user,remember=remember)
            redirect_url = request.args.get("next") or url_for("home")
            return redirect(redirect_url)
        return redirect(url_for("login", incorrect=1))

    else:
        return render_template("login.html")


@app.route('/add-run', methods=["GET","POST"])
@login_required
def add_run():
    if request.method == "POST":
        pass
    else:
        return render_template("add-run.html")




#Static Files: Change Later
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(here + '/static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(here + '/static/css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(here + '/static/img', path)

@app.route('/signup-email/', methods=['POST'])
def signup():
    data = request.form
    print(data["email"])


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def load_user(id):
    u = User.query.get(id)
    return u


if __name__ == '__main__':
    app.run()