import os

import datetime
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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        remember = False
        if request.form.get('rem'):
            remember = True
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember=remember)
            redirect_url = request.args.get("next") or url_for("home")
            return redirect(redirect_url)
        return redirect(url_for("login", incorrect=1))

    else:
        return render_template("login.html")


@app.route('/add-run', methods=["GET", "POST"])
@login_required
def add_run():
    if request.method == "POST":
        run_name = request.form.get("runName")
        location = request.form.get("location")
        image = request.form.get("image")
        pace = request.form.get("paceSel")
        time = request.form.get("time")
        acceptable_pace = ["6 Minute/Mile", "6:30 Minute/Mile","7 Minute/Mile","7:30 Minute/Mile","8 Minute/Mile","8:30 Minute/Mile","9 Minute/Mile","9:30 Minute/Mile","10 Minute/Mile","10:30 Minute/Mile","11 Minute/Mile","11:30 Minute/Mile","12 Minute/Mile","12:30 Minute/Mile","13 Minute/Mile","13:30 Minute/Mile","14 Minute/Mile","14:30 Minute/Mile","15+ Minute/Mile"]
        if not run_name or not location or not image or not (pace in acceptable_pace) or not time:
            return redirect(url_for("add_run", problem=1))
        run = Run()
        run.run_name = run_name
        run.location = location
        run.image_url = image
        run.pace = pace
        run.time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
        run.runners.append(current_user)
        run.owner_id = current_user.id
        db.session.add(run)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("add-run.html")


#TODO: Finish implementing editing a run.
@app.route('/edit-run', methods=["GET", "POST"])
@login_required
def edit_run():
    if request.method == "POST":
        run_name = request.form.get("runName")
        location = request.form.get("location")
        image = request.form.get("image")
        pace = request.form.get("paceSel")
        time = request.form.get("time")
        acceptable_pace = ["6 Minute/Mile", "6:30 Minute/Mile","7 Minute/Mile","7:30 Minute/Mile","8 Minute/Mile","8:30 Minute/Mile","9 Minute/Mile","9:30 Minute/Mile","10 Minute/Mile","10:30 Minute/Mile","11 Minute/Mile","11:30 Minute/Mile","12 Minute/Mile","12:30 Minute/Mile","13 Minute/Mile","13:30 Minute/Mile","14 Minute/Mile","14:30 Minute/Mile","15+ Minute/Mile"]
        if not run_name or not location or not image or not (pace in acceptable_pace) or not time:
            return redirect(url_for("add_run", problem=1))
        run = Run()
        run.run_name = run_name
        run.location = location
        run.image_url = image
        run.pace = pace
        run.time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
        run.runners.append(current_user)
        run.owner_id = current_user.id
        db.session.add(run)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("add-run.html")



@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        if not first_name or not last_name or not email or not password or not cpassword:
            return redirect(url_for("sign_up", problem="Missing a Field"))
        elif password != cpassword:
            return redirect(url_for("sign_up", problem="Passwords don't match!"))
        elif User.query.filter_by(email=email).first():
            return redirect(url_for("sign_up", problem="There is already an account for that email, please login!"))

        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for("home"))

    else:
        return render_template("signup.html")

@app.route("/about-run")
def about_run():
    if request.method == "POST":
        pass
    else:
        if not request.args.get("runid"):
            return redirect(url_for("home"))
        run = Run.query.get(request.args.get("runid"))
        if not run:
            return redirect(url_for("home"))

        if request.args.get("rsvp") and current_user.is_authenticated:
            if current_user in run.runners:
                run.runners.remove(current_user)
            else:
                run.runners.append(current_user)
            db.session.add(run)
            db.session.commit()
            return redirect(url_for("about_run", runid=request.args.get("runid")))

        return render_template("about-run.html", run=run)

# Static Files: Change Later
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
