from flask import Flask, render_template, request

app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'glo_2005_labs'


@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)