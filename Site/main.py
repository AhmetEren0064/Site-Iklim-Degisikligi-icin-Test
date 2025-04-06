from flask import Flask, render_template, request, session, redirect, url_for
from advices import advices_list
from random import choice
import flask_sqlalchemy

app = Flask(__name__)
app.secret_key = "gizli-bir-anahtar"  # oturum desteği için gerekli

#* Veritabanı Ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBNAME.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

#* Veritabanı Modeli
class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    user_password = db.Column(db.String(12), nullable=False)
    user_score = db.Column(db.Integer)

    def __repr__(self):
        return f'<UserScore {self.id}>'

#* Ana Sayfa
@app.route("/", methods=["GET", "POST"])
def adviceCards():
    error = None
    username = session.get("username")

    user = None
    if username:
        user = UserScore.query.filter_by(username=username).first()

    if request.method == "POST":
        action = request.form.get("action")
        form_username = request.form.get("UserName")
        form_password = request.form.get("Password")

        if request.form.get("ive_did") == "clicked":
            if user:
                user.user_score += 10
                db.session.commit() 

        elif action == "register":
            if not form_username or not form_password:
                error = "Kullanıcı adı ve şifre boş olamaz!"
            else:
                new_user = UserScore(username=form_username, user_password=form_password, user_score=0)
                db.session.add(new_user)
                db.session.commit()
                session["username"] = form_username

        elif action == "login":
            if not form_username or not form_password:
                error = "Kullanıcı adı ve şifre boş olamaz!"
            else:
                user = UserScore.query.filter_by(username=form_username, user_password=form_password).first()
                if user:
                    session["username"] = form_username
                else:
                    error = "Giriş başarısız!"

    # Tavsiye kartı
    time_list = ["1 hafta", "2 hafta", "3 hafta", "1 ay", "2 ay"]
    time = choice(time_list)
    random_title = choice(list(advices_list.keys()))
    random_explaning = advices_list[random_title]

    return render_template("index.html",
                           user=user,
                           title=random_title,
                           explaning=random_explaning,
                           time=time,
                           error=error)

#* Çıkış
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("adviceCards"))

if __name__ == "__main__":
    app.run(debug=True)
