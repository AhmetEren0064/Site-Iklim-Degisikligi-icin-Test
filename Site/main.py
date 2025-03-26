from flask import Flask, render_template, request
from advices import advices_list
from random import choice

app = Flask(__name__)



@app.route("/")#todo methods = ["POST"]
def adviceCards():
    score = 0
    title = ""
    explaning = ""
    time_list= ["1 hafta","2 hafta","3 hafta","1 ay","2 ay"]
    time=choice(time_list)
    random_title = choice(list(advices_list.keys()))
    random_explaning = advices_list[random_title]
    return render_template('index.html',
                                score=score,
                                title=random_title,
                                explaning=random_explaning,
                                time=time
                                )
    
""" if request.method == "POST":
        if request.form.get("i_do_already") == "clicked" or request.form.get("another") == "clicked":
            return render_template('index.html',
                                score=score,
                                title=random_title,
                                explaning=random_explaning,
                                time=time
                                )
            
        elif request.form.get("ive-did") == "clicked":
            score+=10
            return render_template('index.html',
                                score=score,
                                title=random_title,
                                explaning=random_explaning,
                                time=time
                                )"""
        
    

if __name__ == "__main__":
    app.run(debug=True)