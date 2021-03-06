from flask import *
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
import sqlite3

app = Flask(__name__)
login_Manager = LoginManager()
login_Manager.init_app(app)
login_Manager.login_view = "home"


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_Manager.user_loader
def load_user(id):
    return User(id)

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        db = sqlite3.connect("database.sqlite3")
        cr = db.cursor()
        email = request.form["email"]
        password = request.form["password"]
        cr.execute("SELECT * from Users WHERE email='" + email +  "' AND password='" +  password +"';")
        data = cr.fetchall()
        if len(data) == 0:
            return redirect(url_for("home"))
        else:
            cr.execute("SELECT UserId, Name, Email from Users WHERE email='" + email + "' AND password='" +  password +"';")
            tuple_data = cr.fetchone()
            id, name, email = tuple_data
            session['user_id'] = id
            session['username'] = name
            session['email'] = email
            login_user(User(id))
            return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/")
def redirectToHome():
    return redirect('/home')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = sqlite3.connect("database.sqlite3")
        cr = db.cursor()
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if len(name) == 0 or len(email) == 0 or len(password) == 0:
            pass
        else:
            cr.execute("INSERT OR IGNORE INTO Users(Name, Email, Password) VALUES(?,?,?);",(name, email, password))
            db.commit()

        if cr.lastrowid == 0:
           return redirect(url_for('register'))
        else:
            return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/welcome")
@login_required
def login():
    return redirect(url_for("profile"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    name = session['username']
    email = session['email']
    info = []
    info.append(name)
    info.append(email)
    return render_template("profile.html", info = info)

if __name__ == "__main__":
    app.secret_key = "yeet123"
    app.run(debug=1)