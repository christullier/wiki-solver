from flask import Flask, render_template, request, redirect, url_for
from main import web_main
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index(): 
    if request.method == "POST":
        article1 = request.form["art1"]
        article2 = request.form["art2"]
        # print(article1, article2)
        return redirect(url_for("solution", start=article1, end=article2))
    else:
        return render_template('index.html')

@app.route("/<start><end>")
def solution(start, end):
    print(start)
    print(end)
    articles = web_main(start, end)
    return f"<h1>solution page <h1> <br></br> <p>articles</p> "

if __name__ == "__main__":
    app.run(debug=True)
