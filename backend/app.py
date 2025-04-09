from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    return render_template("index.html", projects=Project.query.all())

@app.route("/create", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        new_project = Project(title=title, description=description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)