from flask import Flask, render_template, request
from advices import advices_list
from random import choice
import flask_sqlalchemy

app = Flask(__name__)
score = 0

#* Veritabanı
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBNAME.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = flask_sqlalchemy.SQLAlchemy(app)

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    user_password = db.Column(db.String(12), nullable=False)
    user_score = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<UserScore {self.id}>'


#* Sayfalar
@app.route("/", methods=["GET", "POST"])
def adviceCards():
    global score
    if request.method == "POST":
        
        if request.form.get("ive_did") == "clicked":
            score += 10

    title = ""
    explaning = ""
    time_list = ["1 hafta", "2 hafta", "3 hafta", "1 ay", "2 ay"]
    time = choice(time_list)
    random_title = choice(list(advices_list.keys()))
    random_explaning = advices_list[random_title]

    return render_template('index.html',
                           score=score,
                           title=random_title,
                           explaning=random_explaning,
                           time=time)


if __name__ == "__main__":
    app.run(debug=True)